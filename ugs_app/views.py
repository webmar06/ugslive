from django.http import Http404
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.utils import timezone
from .models import UserAccount,UserWallet,Games,Bet,Fight,UserProfile,Commission,Points,UWalletCashout,Longestfight,Stakefund
import datetime,time
import uuid
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils.crypto import get_random_string
from .forms import SignUpForm,LoginForm,UserForm,WalletForm,GameForm,FightForm,LoadPointsForm,SendPoint
from django.core import serializers
from django.core.serializers import serialize
import json
from .serializers import GameSerializer,FightSerializer,UserSerializer
from django.db.models import Sum,Count
from django.utils import timezone

from django_minify_html.middleware import MinifyHtmlMiddleware
from django.http import HttpRequest, HttpResponse

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django.template.loader import render_to_string
from django.http import HttpResponse
from decimal import Decimal
from django.urls import reverse
from datetime import datetime





class ProjectMinifyHtmlMiddleware(MinifyHtmlMiddleware):
    def should_minify(self, request: HttpRequest, response: HttpResponse) -> bool:
        return super().should_minify(request, response) and not request.path.startswith(
            "/admin/"
        )



def index(request):
     # bets=Bet.objects.select_related('fight__f_game').all()
     # ldata=serialize('json',bets)
     # gdata=json.loads(ldata)

     if request.user.is_authenticated:
          return redirect('homepage')
     referral=request.META['HTTP_HOST']+'/agent='+get_random_string(50)
     context={
          'page':'AUTHENTICATION',
          'login_frm':LoginForm()
     }
     return render(request,'ugs_app/auth/index.html',context)


@login_required(login_url='/')
def homepage(request):
     games=Games.objects.filter(g_status='OPEN')
     
     context={
          'page':'HOMEPAGE',
           'games':list(games),
           'ref_url':request.META['HTTP_HOST']+'/registration/',
           'wallet':request.user.userwallet.w_balance
     }
     if request.user.useraccount.usertype == 'SUPER ADMIN':
          return render(request,'ugs_app/homepage/super_admin.html',context)
     elif request.user.useraccount.usertype == 'ADMIN':
          return render(request,'ugs_app/homepage/admin.html',context)
     elif request.user.useraccount.usertype == 'DECLARATOR':
          return render(request,'ugs_app/homepage/declarator.html',context)
     elif request.user.useraccount.usertype == 'PLAYER':
          return render(request,'ugs_app/homepage/player.html',context)
     elif request.user.useraccount.usertype == 'AGENT':
          return render(request,'ugs_app/homepage/agent.html',context)

@login_required(login_url='/')
def games(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'PLAYER':
          games=Games.objects.filter(g_status='OPEN')
          context={
               'page':'GAMES',
               'games':list(games)
          }
          return render(request,'ugs_app/homepage/games.html',context)
    else:
         return redirect(reverse('homepage'))

@login_required(login_url='/')
def setting(request):
     context={
          'page':'SETTING'
     }
     return render(request,'ugs_app/homepage/setting.html',context)

@login_required(login_url='/')
def users(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'SUPER ADMIN':
          users=UserProfile.objects.all().order_by('-date_joined')
          context={
               'page':'USERS',
               'signup_frm':SignUpForm(),
               'user_frm':UserForm(),
               'users':list(users)
          }
          return render(request,'ugs_app/homepage/users.html',context)
     else:
           return redirect(reverse('homepage'))

@csrf_exempt
def upstat(request):
     aid=request.POST.get('acc_id')
     astat=request.POST.get('acc_stat')
     agentcommi=request.POST.get('agentcommi')
     try:
          ucommi=UserAccount.objects.get(user=aid)
          ucommi.status=astat
          ucommi.save()
          
          wcommi=UserWallet.objects.get(user=aid)
          wcommi.commission_rate=agentcommi
          if wcommi.default_rate == 0.000:
             wcommi.default_rate = agentcommi
          wcommi.save()
        
          data='ok'
     except Exception as e:
          data='Error'
     return JsonResponse({'data':data})

@csrf_exempt
def getusers(request):
     acc=UserProfile.objects.all().select_related('useraccount',)
     data=[]
     for a in acc:
          a.date_joined=a.date_joined.strftime("%Y-%m-%d %I:%M %p")
        
          try:
               gwallet=UserWallet.objects.get(user=a)
               wallet=gwallet.w_balance
               comrate=gwallet.commission_rate
          except Exception as e:
               wallet=0
          res={
               'uid':a.id,
               'user':a.username,
               'type':a.useraccount.usertype,
               'agent':str(a.useraccount.user_agent),
               'wallet':wallet,
               'comrate':comrate,
               'status':a.useraccount.status,
               'datejoin':a.date_joined

          }

          data.append(res)
     return JsonResponse({'data':data})
     
     # return JsonResponse(data,safe=False)

def arena(request,game_id):
     fstatus=''
     fid=''
     meron=0
     wala=0
     fnum=0
     mymeronbet=0
     mywalabet=0
     mydrawbet=0
     mylongbet=0
     print(game_id)

     try:
          g_arena=Games.objects.get(g_id=game_id)
          gname=g_arena.g_name
          gid=g_arena.g_id
          meron_name=g_arena.g_redname
          wala_name=g_arena.g_bluename
          video=g_arena.g_link

          try:
               g_fight=Fight.objects.filter(f_game=g_arena).latest('f_created')
               fid=g_fight.f_id
               status=g_fight.f_status
               fnum=g_fight.f_number
               fmulti=g_fight.f_multiplier
               fwin=g_fight.f_winner
               flong=g_fight.f_longest
               try:
                    mymeronbet=Bet.objects.filter(fight=g_fight,status='PENDING',category='MERON',player=request.user).aggregate(total=Sum('amount'))['total']
                    if mymeronbet is None:
                         mymeronbet=0
               except Exception as e:
                    mymeronbet=0
                    
               try:
                    mywalabet=Bet.objects.filter(fight=g_fight,status='PENDING',category='WALA',player=request.user).aggregate(total=Sum('amount'))['total'] 
                    if mywalabet is None:
                         mywalabet=0
               except Exception as e:
                    mywalabet=0
               
               try:
                    mydrawbet=Bet.objects.filter(fight=g_fight,status='PENDING',category='DRAW',player=request.user).aggregate(total=Sum('amount'))['total'] 
                    if mydrawbet is None:
                         mydrawbet=0
               except Exception as e:
                    mydrawbet=0
               try:
                    mylongbet=Longestfight.objects.filter(l_status='WAITING',l_category='LONGEST',l_player=request.user).aggregate(total=Sum('l_amount'))['total'] 
                    if mylongbet is None:
                         mylongbet=0
               except Exception as e:
                    mylongbet=0
               

               try:
                    meron=Bet.objects.filter(fight=fid,category='MERON').aggregate(total=Sum('amount'))['total']
                    if meron is None:
                         meron=0
               except Exception as e:
                    meron=0
               try:
                    wala=Bet.objects.filter(fight=fid,category='WALA').aggregate(total=Sum('amount'))['total'] 
                    if wala is None:
                         wala=0
               except Exception as e:
                    wala=0
               
               

          except Exception as e:
               status='CLOSED'
               fnum=0
               fmulti=0
               fwin=0
               flong=0
               fid=0

     except Exception as e:
          print(e)

     dmeron=float(meron)*float(fmulti)
     dwala=float(wala)*float(fmulti)
     wallet=UserWallet.objects.get(user=request.user)
     wbalance=wallet.w_balance
 
     context={
          'page':'ARENA',
          'game':game_id,
          'game_name':gname,
          'betstat':status,
          'fight_id':fid,
          'fnumber':fnum,
          'wallet':wbalance,
          'mybetmeron':mymeronbet,
          'mybetwala':mywalabet,
          'mydrawbet':mydrawbet,
          'mylongbet':mylongbet,

          'dmeron':dmeron,
          'dwala':dwala,

          'nmeron':meron_name,
          'nwala':wala_name,
          'video':video

     }
     return render(request,'ugs_app/homepage/player_arena.html',context)

@csrf_exempt
def decla_arena(request,game_id):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'DECLARATOR':    
          fform=FightForm()
          fstatus=''
          fid=''
          meron=0
          wala=0
          fnum=0
          try:
               g_arena=Games.objects.get(g_id=game_id)
               gname=g_arena.g_name
               gid=g_arena.g_id
               meron_name=g_arena.g_redname
               wala_name=g_arena.g_bluename
               video=g_arena.g_link

               try:
                    g_fight=Fight.objects.filter(f_game=g_arena).latest('f_created')
                    fid=g_fight.f_id
                    status=g_fight.f_status
                    fnum=g_fight.f_number
                    fmulti=g_fight.f_multiplier
                    fwin=g_fight.f_winner
                    flong=g_fight.f_longest
                    # try:
                    #      mymeronbet=Bet.objects.filter(fight=g_fight,status='PENDING',category='MERON',player=request.user).aggregate(total=Sum('amount'))['total']
                    #      if mymeronbet is None:
                    #           mymeronbet=0
                    # except Exception as e:
                    #      mymeronbet=0
                         
                    # try:
                    #      mywalabet=Bet.objects.filter(fight=g_fight,status='PENDING',category='WALA',player=request.user).aggregate(total=Sum('amount'))['total'] 
                    #      if mywalabet is None:
                    #           mywalabet=0
                    # except Exception as e:
                    #      mywalabet=0

                    try:
                         meron=Bet.objects.filter(fight=fid,category='MERON').aggregate(total=Sum('amount'))['total']
                         if meron is None:
                              meron=0
                    except Exception as e:
                         meron=0
                    try:
                         wala=Bet.objects.filter(fight=fid,category='WALA').aggregate(total=Sum('amount'))['total'] 
                         if wala is None:
                              wala=0
                    except Exception as e:
                         wala=0
                    try:
                         draw=Bet.objects.filter(fight=fid,category='DRAW').aggregate(total=Sum('amount'))['total'] 
                         if draw is None:
                              draw=0
                    except Exception as e:
                         draw=0

                    try:
                         long=Longestfight.objects.filter(l_status='WAITING',l_category='LONGEST').aggregate(total=Sum('l_amount'))['total']
                         clong=Longestfight.objects.filter(l_status='WAITING',l_category='LONGEST').aggregate(total=Count('id'))['total'] 
                         if long is None or clong is None:
                              long=0
                              clong=0
                    except Exception as e:
                         long=0
                         clong=0

               except Exception as e:
                    status='NONE'
                    fnum=0
                    fmulti=0
                    fwin=0
                    flong=0
                    fid=0
                    draw=0
                    long=0
                    clong=0


          except Exception as e:
               print(e)
          
          dmeron=float(meron)*float(fmulti)
          dwala=float(wala)*float(fmulti)
          wallet=UserWallet.objects.get(user=request.user)
          wbalance=wallet.w_balance
     
          context={
               'page':'DECLA ARENA',
               'game':game_id,
               'game_name':gname,
               'meron':meron,
               'wala':wala,
               'draw':draw,
               'long':long,
               'status':status,
               'fnum':fnum,
               'fwin':fwin,
               'flong':flong,
               'multiplier':fmulti,
               'fform':fform,
               'fight_id':fid,
               'wallet':wbalance,
               # 'mybetmeron':mymeronbet,
               # 'mybetwala':mywalabet,
               'dmeron':dmeron,
               'dwala':dwala,
               'nmeron':meron_name,
               'nwala':wala_name,
               'clong':clong,
               'video':video
          }
          return render(request,'ugs_app/homepage/decla_arena.html',context)
     else:
         return redirect(reverse('homepage'))





# DECLARATOR
@csrf_exempt
def delgame(request):
     did=request.POST.get('did')
     dgames=Games.objects.get(g_id=did).delete()
     if dgames:
          data='ok'
     else:
          data='Failed'
     return JsonResponse({'data':data})



@csrf_exempt
def gfight(request):
     gid=request.POST.get('gfid')
     game=Games.objects.get(g_id=gid)
     try:
          gf=Fight.objects.filter(f_game=game).latest('f_created')
          fid=gf.f_id
          fnum=gf.f_number
          fmulti=gf.f_multiplier
          fstat=gf.f_status
          fwin=gf.f_winner
          flong=gf.f_longest
     except Exception as e:
          fid=0
          fnum=0
          fmulti=0
          fwin=''
          flong=0
          fstat='CLOSED'
 
     data={
          'game':game.g_id,
          'fight':fid,
          'fnum':fnum,
          'fmulti':fmulti,
          'fstat':fstat,
          'fwin':fwin,
          'flong':flong
     }
     
     return JsonResponse({'data':data})




@csrf_exempt
def addfight(request):
     fform=FightForm(request.POST or None)
     gid=request.POST.get('fgame')
     f_id=request.POST.get('f_id')
     typ=request.POST.get('f_type')
     code=get_random_string(6)
     fnum=request.POST.get('f_number')
  
          
     if typ is None:
          try:
               ckfight=Fight.objects.get(f_id=f_id,f_number=fnum)
               data='exist'
          except Exception as e:
           if fform.is_valid():
               nf = fform.save(commit=False)
               nf.f_code=code
               nf.f_status='CLOSED'
               nf.save()
               data='insert'
           else:
               data='Invalid Form'
     else:
          try:
               gf=Fight.objects.get(f_id=f_id)
               gf.f_number=request.POST.get('f_number')
               gf.f_multiplier=request.POST.get('f_multiplier')
               gf.save()
               data='update'
          except Exception as e:
               print(e)
               data='Not Found'
  
     return JsonResponse({'data':data})



@login_required(login_url='/')
def decla_games(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'DECLARATOR':
          games=Games.objects.all().filter()
          for g in games:
               g.g_created = g.g_created.strftime("%Y-%m-%d %I:%M %p")
          context={
               'page':'DECLA GAMES',
               'game_frm':GameForm(),
               'games':list(games)
          }
          return render(request,'ugs_app/homepage/decla_games.html',context)
     else:
         return redirect(reverse('homepage'))

@csrf_exempt
def load_games(request):
     ggames=Games.objects.all().order_by('-g_created')
     # for g in ggames:
     #      g.g_created = g.g_created.strftime("%Y-%m-%d %I:%M %p")
     ldata=serialize('json',ggames)
     gdata=json.loads(ldata)
     return JsonResponse(gdata,safe=False)


@csrf_exempt
def getgame(request):
     gid=request.POST.get('gid')
     upgames=Games.objects.get(g_id=gid)
     # data=upgames
     # ldata=serialize('json',upgames)
     # data=json.loads(ldata)
     data={
          'gname':upgames.g_name,
          'meron':upgames.g_redname,
          'wala':upgames.g_bluename,
          'plasada':upgames.g_plasada,
          'desc':upgames.g_desc,
          'category':upgames.g_category,
          'link':upgames.g_link,
          'image':str(upgames.g_image),
          'status':upgames.g_status    
     }
     return JsonResponse({'data':data})

# declarator
@csrf_exempt
def add_games(request):
     if request.method =='POST':
          gform=GameForm(request.POST, request.FILES)
          if gform.is_valid():
               games = gform.save(commit=False)
               # games.g_created=datetime.datetime.now()
               games.g_by=request.user.id
               games.save()
               data='ok'
          else:
               data='bad'
        
     return JsonResponse({'data':str(data)})

# declarator
@csrf_exempt
def update_games(request):
     if request.method =='POST':
          gform=GameForm(request.POST, request.FILES)
          games=Games.objects.get(g_id=request.POST.get('g_id'))
          if request.FILES.get('g_image') is None:
               games.g_name=request.POST.get('g_name')
               games.g_redname=request.POST.get('g_redname')
               games.g_bluename=request.POST.get('g_bluename')
               games.g_plasada=request.POST.get('g_plasada')
               games.g_desc=request.POST.get('g_desc')
               games.g_category=request.POST.get('g_category')
               games.g_link=request.POST.get('g_link')
               games.g_status=request.POST.get('g_status')
               games.save()
               data='ok'
          else:
               if gform.is_valid():
                    games.g_image=request.FILES.get('g_image')
                    games.g_name=request.POST.get('g_name')
                    games.g_redname=request.POST.get('g_redname')
                    games.g_bluename=request.POST.get('g_bluename')
                    games.g_plasada=request.POST.get('g_plasada')
                    games.g_desc=request.POST.get('g_desc')
                    games.g_category=request.POST.get('g_category')
                    games.g_link=request.POST.get('g_link')
                    games.g_status=request.POST.get('g_status')
                    games.save()
                    data='ok'
               else:
                    data='Not Valid'

     return JsonResponse({'data':str(data)})

@csrf_exempt
def auth_user(request):
     form = LoginForm(request.POST or None)
     msg=''
     if request.method == 'POST':
          if form.is_valid():
               username=form.cleaned_data.get('username')
               password=form.cleaned_data.get('password')
               user=authenticate(username=username, password=password)
               if user is not None:
                    if user.useraccount.status == 'INACTIVE':
                         msg='inactive'
                    else:
                         request.session['usertype'] = user.useraccount.usertype
                         msg='login'
                         login(request,user)
                         status=1
               else:
                    status=0
                    msg='err'
          else:
              status=0
              msg='not valid'

     return JsonResponse({'data':msg})


def signout(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def account_reg(request):
    code=get_random_string(10)
    referral_link=request.META['HTTP_HOST']+'/registration/'+code
    token=get_random_string(6)
    form=SignUpForm()
    userform=UserForm()
    walletform=WalletForm()
    if request.method=='POST':
       account = SignUpForm(data=request.POST)
       userinfo = UserForm(data=request.POST)
     #   wallet=WalletForm(data=request.POST)
     #   print(request.POST.get('contact_no'))
       if account.is_valid() and userinfo.is_valid() :
            user = account.save()
            user.set_password(user.password)
            user.save()
            info = userinfo.save(commit = False)
            info.user = user
            info.usertype=request.POST.get('usertype')
            info.relpass=request.POST.get('password')
            info.referral_code=code
            info.referral_link=referral_link
            info.user_agent=request.user
            info.status='INACTIVE'
            info.save()
            wall=walletform.save(commit = False)
            wall.user=user
            wall.w_balance=0
            wall.w_points=0
            wall.w_commission=0
            wall.w_status='ACTIVE'
            wall.save()
            data='ok'
           
       else:
            data='Error Validating'
    else:
          data=request

    return JsonResponse({'data':data})



@csrf_exempt
def lastcall(request):
     gfid=request.POST.get('gfight')
     # print(gfid)
     cfight=Fight.objects.get(f_id=gfid)
     cfight.f_status='LAST CALL'
     cfight.save()
     data=cfight.f_status
     return JsonResponse({'data':data})

@csrf_exempt
def closebet(request):
     gfid=request.POST.get('cfight')
 
     cfight=Fight.objects.get(f_id=gfid)
     cfight.f_status='CLOSE'
     cfight.save()
     data=cfight.f_status
     return JsonResponse({'data':data})

@csrf_exempt
def openbet(request):
     ofid=request.POST.get('ofight')

     cfight=Fight.objects.get(f_id=ofid)
     cfight.f_status='DONE'
     cfight.save()
     game=cfight.f_game
     fnum=cfight.f_number
     addf=Fight(f_number=fnum +1,f_game=game,f_winner='',f_status='OPEN').save()
     
     data=cfight.f_status
     return JsonResponse({'data':data})






@csrf_exempt
def revert(request):
     fid=request.POST.get('fight')
     try:
          gfight=Fight.objects.get(f_id=fid)
          gfight.f_winner=''
          gfight.f_status='CLOSING'
          gfight.save()
          data='ok'
     except Exception as e:
          data='bad'
 
     return JsonResponse({'data':data})





@csrf_exempt
def nxtfight(request):
     fid=request.POST.get('fight')
     gid=request.POST.get('game')
     multi=request.POST.get('multi')
     code=get_random_string(6)
     fform=FightForm()
     try:
          ggame=Games.objects.get(g_id=gid)
          try:
               gfight=Fight.objects.get(f_id=fid)
               fnum=gfight.f_number
               # data=fnum
               nwf = fform
               if nwf.is_valid:
                    nf = fform.save(commit=False)   
                    nf.f_game=ggame 
                    nf.f_number=fnum + 1
                    nf.f_multiplier=multi
                    nf.f_code=code
                    nf.f_status='CLOSED'
                    nf.save()
                    data='ok'
          except Exception as e:
               data='bad fight'
     except Exception as e:
          data='bad'
     return JsonResponse({'data':data})

# ////////////////////////////////



def registration(request,code):
     agent=UserAccount.objects.get(referral_code=code)
     context={
          'page':'REGISTRATION',
          'code':code,
          'signup_frm':SignUpForm(),
          'user_frm':UserForm()
     
     }
     return render(request,'ugs_app/auth/registration.html',context)

@csrf_exempt
def player_reg(request):
     code=get_random_string(150)
     referral_link=request.META['HTTP_HOST']+'/registration/'+code
     walletform=WalletForm()
     account = SignUpForm(data=request.POST)
     userinfo=UserForm()

     aid=request.POST.get('code')
     try:
          agent=UserAccount.objects.get(referral_code=aid)
          if agent is not None:
               data='Exist'
               if account.is_valid():
                    user = account.save()
                    user.set_password(user.password)
                    user.save()
                    info = userinfo.save(commit = False)
                    info.user = user
                    info.usertype='PLAYER'
                    info.relpass=request.POST.get('password')
                    info.referral_code=code
                    info.referral_link=referral_link
                    info.user_agent=agent.user
                    info.status='INACTIVE'
                    info.save()
                    wall=walletform.save(commit = False)
                    wall.user=user
                    wall.w_balance=0
                    wall.w_points=0
                    wall.w_commission=0
                    wall.w_status='ACTIVE'
                    wall.save()
                    data='ok'
               else:
                    data='Form Not Valid'

     except Exception as e:
          data='Referral Agent Not Found!'

     

     return JsonResponse({'data':data})

@csrf_exempt
def uppass(request):
     account = SignUpForm(request.POST, instance=request.user)
     curpassword=request.POST.get('curpass')
     password=request.POST.get('password')

     useracc=authenticate(username=request.user.username, password=curpassword)
     if useracc is not None:
          if account.is_valid():
               user = account.save()
               user.set_password(user.password)  
               user.save()
               login(request,user)
               data='ok'
          else:
               data='Invalid Form'
     else:
          data='Invalid Password'

     return JsonResponse({'data':data})


def timer(request):
     return render(request,'ugs_app/timer.html')


# ADMIN
@login_required(login_url='/')
def mydownlines(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'ADMIN':
          myagent=UserProfile.objects.all().select_related('useraccount')
          context={
               'page':'DOWNLINES',
               'signup_frm':SignUpForm(),
               'user_frm':UserForm(),
               'users':myagent
          }
          return render(request,'ugs_app/homepage/mydownline.html',context)
     else:
         return redirect(reverse('homepage'))


















# -------------------mmmmmmmm---------------------------
@login_required(login_url='/')
def admin_points(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'SUPER ADMIN':
         user_id = request.user.id
         adminPointsList = Points.objects.select_related('p_sender').filter(p_sender=user_id)
         context = {
            'page': 'adminloadPoints',
            'adminPointsList': adminPointsList,
            'SendPoint': SendPoint(),
        }
         return render(request, 'ugs_app/homepage/admin_load_points.html', context)
    else:
         return redirect(reverse('homepage'))
    
      

@csrf_exempt
def loadAdminPoints(request):
    if request.method == 'POST':
        code_point = get_random_string(12)
        code_points = code_point.upper()
        pointsend = request.POST.get('load_amount')
        receiver=UserProfile.objects.get(id=request.POST.get('user_agent'))

        if float(pointsend) >0:
               form = SendPoint(request.POST)
               if form.is_valid():
                    try:
                         points = form.save(commit=False)
                         points.p_sender=request.user
                         points.p_receiver=receiver
                         points.p_code=code_points
                         points.p_amount=request.POST.get('load_amount')
                         points.save()
                         data='ok'
                    except Exception as e:
                         data='Error'

                    try:
                         pwallet=UserWallet.objects.get(user=receiver)
                         curbalance=pwallet.w_balance
                         pointbal=pwallet.w_points
                         newbal=float(curbalance) + float(pointsend)
                         newpoint=float(pointbal) + float(pointsend)
                         pwallet.w_balance=newbal
                         pwallet.w_points=newpoint
                         pwallet.save() 
                         data='ok'
                    except Exception as e:
                         data='Error'

                    return JsonResponse({'data': data})
               else: 
                    return JsonResponse({'data': 'error', 'errors': form.errors})
        else:
             return JsonResponse({'data': 'invalid'})
    return JsonResponse({'data': 'invalid method'})

@login_required(login_url='/')
def load_adpoints_table(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'SUPER ADMIN':
          user_id = request.user.id
          adminPointsList = Points.objects.select_related('p_sender').filter(p_sender=user_id)
          context = {
               'page': 'adminloadPoints',
               'adminPointsList': adminPointsList,
               'SendPoint': SendPoint(),
          }
          html_content = render_to_string('ugs_app/homepage/load_adpoints_table.html', context)
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))


@login_required(login_url='/')
def agentplayer(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'AGENT':
          users=[]
          myusers = UserProfile.objects.select_related('useraccount')
     
          for u in myusers:
               if u.useraccount.user_agent == request.user:
                    users.append(u)
               context={
               'mycommi':request.user,
               'page':'AGENTPLAYER',
               'users':list(users)
          }
          return render(request,'ugs_app/homepage/agentplayer.html',context)
     else:
          return redirect(reverse('homepage'))
     
     
@csrf_exempt
def upplyrstat(request):
     aid=request.POST.get('acct_id')
     astat=request.POST.get('plstatus')
     comirate=request.POST.get('commirate')
     commi=request.POST.get('commission')
     agentid=request.POST.get('agentid')

     userplayer=UserAccount.objects.get(user=aid)
     usertype = userplayer.usertype

     ccommi=UserWallet.objects.get(user=aid)
     curcommi = ccommi.commission_rate

     acommi=UserWallet.objects.get(user=agentid)
     aurcommi = acommi.commission_rate

     if usertype == 'AGENT':
          comminf   = Decimal(commi)
          curcommif = Decimal(curcommi)
          aurcommif = Decimal(aurcommi)
          modulo    = curcommif-comminf

          if aurcommi>=comminf: 
               nwcommi = aurcommif+modulo
               try:
                    ucommi=UserAccount.objects.get(user=aid)
                    ucommi.status=astat
                    ucommi.save()
          
                    wcommi=UserWallet.objects.get(user=aid)
                    wcommi.commission_rate=commi
                    if wcommi.default_rate == 0.000:
                       wcommi.default_rate = commi
                    wcommi.save()

                    nwcomi=UserWallet.objects.get(user=agentid)
                    nwcomi.commission_rate=nwcommi
                    nwcomi.save()
                    data='ok'
               except Exception as e:
                   data='Error'
          else:
            data='Error'
     else:
          try:
             ucommi=UserAccount.objects.get(user=aid)
             ucommi.status=astat
             ucommi.save()
             nwcommi = aurcommi
             data='ok'
          except Exception as e:
           data='Error'
     
     return JsonResponse({'data':data, 'nwcommi':nwcommi})


@login_required(login_url='/')
def load_new_user(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'AGENT':
          users=[]
          myusers = UserProfile.objects.select_related('useraccount')
          for u in myusers:
               if u.useraccount.user_agent == request.user:
                    users.append(u)
               context={
               'page':'AGENTPLAYER',
               'users':list(users)
          }
          html_content = render_to_string('ugs_app/homepage/agentplayer_table.html', context)    
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))


@login_required(login_url='/')
def load_points(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'AGENT':
          agentPointsList = Points.objects.select_related('p_sender').all()
          context = {
               'page': 'LOAD POINTS',
               'agentPointsList': agentPointsList,
               'LoadPointsForm': LoadPointsForm(),
          }
          return render(request, 'ugs_app/homepage/load_points.html', context)
    else:
         return redirect(reverse('homepage'))
    



@csrf_exempt
def loadAgentPoints(request):
    if request.method == 'POST':
        code_point = get_random_string(12)
        code_points = code_point.upper()
        pointsend = request.POST.get('load_amount')
        receiver=UserProfile.objects.get(id=request.POST.get('user_agent'))
        apwallet=UserWallet.objects.get(user=request.user)
        acurbalance=apwallet.w_balance
        apointbal=apwallet.w_points

        fromsender = str(request.user.id)
        toreveiver = str(request.POST.get('user_agent'))

        if fromsender != toreveiver:
             if float(pointsend) >0:
                    if float(acurbalance) >= float(pointsend):
                         form = LoadPointsForm(request.POST)
                         if form.is_valid():
                              try:
                                   points = form.save(commit=False)
                                   points.p_sender=request.user
                                   points.p_receiver=receiver
                                   points.p_code=code_points
                                   points.p_amount=request.POST.get('load_amount')
                                   points.save()
                                   data='ok'
                              except Exception as e:
                                   data='Error'

                              try:
                                   pwallet=UserWallet.objects.get(user=receiver)
                                   curbalance=pwallet.w_balance
                                   pointbal=pwallet.w_points
                                   newbal=float(curbalance) + float(pointsend)
                                   newpoint=float(pointbal) + float(pointsend)
                                   pwallet.w_balance=newbal
                                   pwallet.w_points=newpoint
                                   pwallet.save() 
                                   data='ok'
                              except Exception as e:
                                   data='Error'

                              try:
                                   anewbal=float(acurbalance) - float(pointsend)
                                   anewpoint = float(apointbal) - float(pointsend)
                                   if float(anewbal) >0:
                                       anewbals = anewbal
                                   else:
                                       anewbals = 0
                                   
                                   if float(anewpoint) >0:
                                       anewpoints = anewpoint
                                   else:
                                       anewpoints = 0
                         
                                   apwallet.w_balance=anewbals
                                   apwallet.save() 
                                   data='ok'
                                   newpoints = anewbals
                              except Exception as e:
                                   data='Error'

                              return JsonResponse({'data': data, 'newpoints': newpoints})
                         else: 
                              newpoints = acurbalance
                              return JsonResponse({'data': 'error', 'newpoints': newpoints, 'errors': form.errors})
                    else:
                         newpoints = acurbalance
                         return JsonResponse({'data': 'insufficient', 'newpoints': newpoints})
             else:
                    newpoints = acurbalance
                    return JsonResponse({'data': 'invalid', 'newpoints': newpoints})
        else:
           newpoints = acurbalance
           return JsonResponse({'data': 'invalid', 'newpoints': newpoints})
  
    return JsonResponse({'data': 'invalid method'})



@login_required(login_url='/')
def load_points_table(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'AGENT':
          agentPointsList = Points.objects.select_related('p_sender').all()
          context = {
               'page': 'LOAD POINTS',
               'agentPointsList': agentPointsList,
               'LoadPointsForm': LoadPointsForm(),
          }
          html_content = render_to_string('ugs_app/homepage/load_points_table.html', context)
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))



# fight history
def get_fight_data(request):
    try:
        fights = Fight.objects.all().order_by('f_number').values('f_number', 'f_winner','f_tblrows')
        fight_list = list(fights)
        return JsonResponse(fight_list, safe=False)
    except Exception as e:
        print(f"Error fetching fight data: {e}")
        return JsonResponse({'error': str(e)}, status=500)
#    fight history







# reglahan set winner
@csrf_exempt
def setwinner(request):
    fid = request.POST.get('fight')
    winner = request.POST.get('winner')
    gameid = request.POST.get('gameid')
    try:
        drawfight = Fight.objects.filter(f_game=gameid, f_status='DONE').exclude(f_winner='DRAW').exclude(f_winner='CANCELLED').order_by('-f_number').first()
        gfight    = Fight.objects.filter(f_game=gameid, f_status='DONE').order_by('-f_number').first()
        fightnum  = Fight.objects.filter(f_game=gameid).order_by('-f_number').first()
        if gfight:
            fnumber = gfight.f_number
            prevWinner = gfight.f_winner
            prevColumn = gfight.f_tblrows
            currentfnum = fightnum.f_number
            prevDrawWin  = drawfight.f_winner

            game = Games.objects.get(g_id=gameid)
            gamecol = game.g_col
            
            colhistory = prevColumn
            colControl = gamecol
            
            # update plus 5 new column
            if colhistory > colControl:
                newColControl = colControl + 5
            else:
                newColControl = colControl

            ngame = Games.objects.get(g_id=gameid)
            ngame.g_col=newColControl
            ngame.save()
            # update plus 5 new column
            
            if currentfnum > 1:
                if prevWinner == winner or prevWinner == 'DRAW' and winner ==  prevDrawWin or prevWinner == 'CANCELLED' and winner ==  prevDrawWin:
                    newColHistory = colhistory + 1
                elif winner == 'DRAW':
                    newColHistory = colhistory + 1
                elif winner == 'CANCELLED':
                    newColHistory = colhistory + 1
                elif prevWinner == winner and  colhistory == colControl:
                    newColHistory = colhistory + 1
                elif prevWinner != winner and  colhistory == colControl:
                    newColHistory = colhistory + 5
                else:
                    manipulate = newColControl-colhistory
                    newColHistory = manipulate + colhistory
            else:
                newColHistory = 1;
            
            gfight = Fight.objects.get(f_id=fid)
            gfight.f_winner = winner
            gfight.f_status='DECLARED'
            gfight.f_tblrows=newColHistory
            gfight.save() 
            data = 'ok'
        else:
          gfights = Fight.objects.get(f_id=fid)
          gfights.f_winner = winner
          gfights.f_status='DECLARED'
          gfights.f_tblrows=1
          gfights.save() 
          
          data = 'ok'
    except Exception as e:
        print(e)
        data = 'bad'    
    return JsonResponse({'data': data})











# disbusement
# upline commission - disbuse
@csrf_exempt
def disburse(request):
    fid = request.POST.get('fight')
    try:
        if not fid:
            raise ValueError("Fight ID is required")

        gfight = Fight.objects.get(f_id=fid)
        gfight.f_status = 'DONE'
        gfight.save()

        bets = Bet.objects.filter(fight=gfight, winStat=0)
        if not bets.exists():
            raise ValueError("No bets found for this fight")

        for bet in bets:
          # UPDATE WINNER AMOUNT
          if gfight.f_winner != 'CANCELLED':
               if gfight.f_winner == bet.category:
                  betstat = 'WIN'
                  wonamount = bet.winning_amnt
               # DISTRIBUTE WON AMOUNT ON PLAYER
                  Bet.objects.filter(id=bet.id, status='PENDING').update(won_amnt = wonamount, status=betstat, winStat=1)
                  gwallet=UserWallet.objects.get(user=bet.player.id)
                  curbalance=gwallet.w_balance
                  pointbal=gwallet.w_betwins
                  newbal=float(curbalance) + float(wonamount)
                  newpoint=int(pointbal) + float(wonamount)
                  gwallet.w_balance=newbal
                  gwallet.w_betwins=newpoint
                  gwallet.save() 
               # DISTRIBUTE WON AMOUNT ON PLAYER
               else:
                  betstat = 'LOSE'
                  wonamount = 0
                  Bet.objects.filter(id=bet.id, status='PENDING').update(won_amnt = wonamount, status=betstat, winStat=1)
                  

               commi_distrib = distribute_commission_upward(bet.player.id, bet.amount)
               for commission_data in commi_distrib:
                 if commission_data['user_id'] == bet.player.id or commission_data['commission'] == 0:
                    continue
                 if gfight.f_winner == bet.category:
                    commission = Commission(
                        c_fight=gfight,
                        c_fnumber=gfight.f_number,
                        c_player=bet.player.id,
                        c_betamnt=bet.amount,
                        c_winner=gfight.f_winner,
                        c_commission=commission_data['commission'],
                        c_agent=commission_data['user_id'],
                    )
                    commission.save()
                    
                    try:
                         with transaction.atomic():
                              pwallet = UserWallet.objects.select_for_update().get(user=commission_data['user_id'])
                              curbalance = float(pwallet.w_balance)
                              combalance = float(pwallet.w_commission) 
                              newbal = curbalance + float(commission_data['commission'])
                              newcom = combalance + float(commission_data['commission'])

                              pwallet.w_balance = newbal
                              pwallet.w_commission = newcom
                              pwallet.save()
                    except ObjectDoesNotExist:
                         print(f"UserWallet for user {commission_data['user_id']} does not exist.")
                    except Exception as e:
                         print(f"An error occurred while updating UserWallet: {e}")
                         data = 'ok'
          else:
               refundamnt = bet.amount
               betstat = 'CANCELLED'
               wonamount = 0
               Bet.objects.filter(id=bet.id, status='PENDING').update(amount = 0, winning_amnt=0, won_amnt = wonamount, status=betstat, winStat=2)

               clwallet=UserWallet.objects.get(user=bet.player.id)
               curbal=clwallet.w_balance
               pointbal=clwallet.w_betwins
               newbals=float(curbal) + float(refundamnt)
               newpoint=float(pointbal) + float(refundamnt)
               clwallet.w_balance=newbals
               clwallet.save()

          data = 'ok'
    except Exception as e:
        data = f"Error: {e}"
    return JsonResponse({'data': data})




def distribute_commission_upward(user_id, bet_amount): 
    commi_distrib = []
    visited = set()
    distribute_upward(user_id, bet_amount, commi_distrib, visited)
    return commi_distrib

def distribute_upward(user_id, bet_amount, commi_distrib, visited):
    if user_id in visited:
        return
    visited.add(user_id)

    try:
        user_account = UserAccount.objects.get(user_id=user_id)
        user_wallet = UserWallet.objects.get(user=user_account.user)
        user_commission_rate = float(user_wallet.commission_rate)
        user_commission = bet_amount * user_commission_rate

        commi_distrib.append({
            'user_id': user_id,
            'commission': user_commission
        })
     #    print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')
     #    print(user_id)
     #    print(bet_amount)
     #    print(user_commission_rate)
     #    print(user_commission)
     #    print(commi_distrib)
     #    print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')

        if user_account.user_agent_id:
            distribute_upward(user_account.user_agent_id, bet_amount, commi_distrib, visited)
    except UserAccount.DoesNotExist:
        print(f"User account with user_id {user_id} does not exist.")
        commi_distrib.append({'user_id': user_id, 'commission': 0})
    except UserWallet.DoesNotExist:
        print(f"User wallet for user_id {user_id} does not exist.")
        commi_distrib.append({'user_id': user_id, 'commission': 0})



















        # DECLA UPDATE FIGHT STATUS /////////
@csrf_exempt
def fight_stat(request):
    fid = request.POST.get('fid')
    typ = request.POST.get('typ')
    data = 0
    mymeronbet = 0
    mywalabet = 0
    try:
        fight = Fight.objects.get(f_id=fid)
        fight.f_status = typ
     #    fight.f_status = 'LAST CALL'
        fight.save()
        
        if typ == 'CLOSING':
            bets = Bet.objects.filter(fight=fight)
            if not bets.exists():
                raise ValueError("No bets found for this fight")

            try:
                game_room = fight.f_game
                cgame = Games.objects.get(g_id=game_room)
                plasada = cgame.g_plasada
            except Games.DoesNotExist:
                plasada = 0
            except Exception as e:
                plasada = 0

            try:
                gf = Fight.objects.filter(f_game=game_room).latest('f_created')
                fid = gf.f_id
                fmulti = gf.f_multiplier
                status = gf.f_status
                game_num = gf.f_number
                winner = gf.f_winner
            except Exception as e:
                fid = 0
                status = ''
                game_num = 0
                fmulti = 0
                winner = ''

            try:
                meron = Bet.objects.filter(fight=fid, category='MERON').aggregate(total=Sum('amount'))['total']
                if meron is None:
                    meron = 0
            except Exception as e:
                meron = 0

            try:
                wala = Bet.objects.filter(fight=fid, category='WALA').aggregate(total=Sum('amount'))['total']
                if wala is None:
                    wala = 0
            except Exception as e:
                wala = 0

            # COMPUTATION
            totmw = meron + wala
            # PLASADA
            totpla = float(plasada) * float(totmw)
            lesspla = totmw - totpla

            if meron > 0:
                meronlesspla = lesspla / meron
            else:
                meronlesspla = lesspla

            if wala > 0:
                walalesspla = lesspla / wala
                walapayout = walalesspla * 100
            else:
                walalesspla = lesspla
                walapayout = walalesspla * 100

            meronpayout = meronlesspla * 100

            # odds
            meronodds = meronpayout * 0.01
            walaodds = walapayout * 0.01

            for bet in bets:
                try:
                    mymeronbet = Bet.objects.filter(
                        fight=fid, 
                        status='PENDING', 
                        category='MERON', 
                        player=bet.player.id
                    ).aggregate(total=Sum('amount'))['total']
                    if mymeronbet is None:
                        mymeronbet = 0
                except Exception as e:
                    mymeronbet = 0

                try:
                    mywalabet = Bet.objects.filter(
                        fight=fid, 
                        status='PENDING', 
                        category='WALA', 
                        player=bet.player.id
                    ).aggregate(total=Sum('amount'))['total']
                    if mywalabet is None:
                        mywalabet = 0
                except Exception as e:
                    mywalabet = 0

                # Calculate the winnings
                merontowin = meronodds * mymeronbet
                walatowin = walaodds * mywalabet
                # player dummy total bet
                dmeron = fmulti * meron
                dwala = fmulti * wala

               #  print('xxxxxxxxxxxxxxxxxxxxxxxxxx')
                if bet.category == 'MERON':
                     winning_bet = meronpayout
                elif  bet.category == 'WALA':
                     winning_bet = walapayout
                elif  bet.category == 'LONGEST':
                     winning_bet = 0
                elif  bet.category == 'DRAW':
                     winning_bet = walapayout*8
                     
                  
               #  print(f"Bet ID: {bet.id}, Bettor ID: {bet.player.id}, Bettor: {bet.player.username}, Player bet amount: {mymeronbet}, Bet: {bet.category}, Payout : {winning_bet}")
               #  SAVE WINNING BET AMOUNT
                Bet.objects.filter(id=bet.id, winStat=0).update(winning_amnt = winning_bet)
               #  SAVE WINNING BET AMOUNT
        data = 1     
    except Fight.DoesNotExist:
        data = 0
     #    print(f"Fight with ID {fid} does not exist.")

    except Exception as e:
     #    print(f"Error: {e}")
        data = 0

    return JsonResponse({'data': data})



@csrf_exempt
def updatewallet(request):
     amount=request.POST.get('amount')
     ttrans=request.POST.get('ttype')
     fid=request.POST.get('fid')
     betin=request.POST.get('betin')
    
     try:
          gwallet=UserWallet.objects.get(user=request.user)
          curbalance=gwallet.w_balance
          newbal=float(curbalance) - float(amount)
          gwallet.w_balance=newbal
          gwallet.save()
          try: 
               fight=Fight.objects.get(f_id=fid)
               try:
                    if betin == 'LONGEST':
                        bet=Longestfight.objects.create(l_fight=fight,l_amount=amount,l_category=betin,l_player=request.user,l_fightno=fight.f_number)
                    else:
                        bet=Bet.objects.create(fight=fight,amount=amount,category=betin,player=request.user,fightno=fight.f_number) 
                    
               except Exception as e:
                    print(e)
          except Exception as e:
               print(e)
     except Exception as e:
          print(e)

     data=gwallet.w_balance
     return JsonResponse({'data':data})



# @csrf_exempt
# def addfight(request):
#     data = '' 
#     if request.method == 'POST':
#         post_data = request.POST.copy()
#         if not post_data.get('f_tblrows'):
#             post_data['f_tblrows'] = 1
        
#         fform = FightForm(post_data)
#         if fform.is_valid():
#             try:
#                 nf = fform.save(commit=False)
#                 nf.f_id = uuid.uuid4()
#                 nf.f_code = get_random_string(6)
#                 nf.f_status = 'CLOSED'
#                 nf.save()
#                 data = 'insert'
#             except Exception as e:
#                 print(e)
#                 data = str(e)
#         else:
#             print(fform.errors)
#             data = fform.errors.as_json()
#     else:
#         fform = FightForm()

#     return render(request, 'ugs_app/homepage/decla_games.html', {'fform': fform, 'data': data})

@csrf_exempt
def cashoutwallet(request):
    if request.method == 'POST':
        code_point = get_random_string(12)
        code_cashout = code_point.upper()
        cashout = request.POST.get('cashout')
        status = "invalid" 
     
        agent=UserAccount.objects.get(user=request.user.id)
        pwallet=UserWallet.objects.get(user=request.user.id)
        curbalance=pwallet.w_balance
        tlcashout=pwallet.wallet_out
        agentid = agent.user_agent.id
        newtotalout = tlcashout
        
        try:
          hwallet = UWalletCashout.objects.filter(cw_player=request.user).order_by('-cw_created').first()
          if hwallet:
             lastdate = hwallet.cw_created
          else:
             lastdate = 'NotExist'
        except UWalletCashout.DoesNotExist:
           lastdate = 'NotExist'
          
        if float(cashout)>0:
               if float(curbalance) >= float(cashout):
                    if lastdate !='NotExist':
                         if lastdate.tzinfo is None:
                              date1 = timezone.make_aware(lastdate, timezone.get_current_timezone())
                         else:
                              date1 = lastdate
                              date2 = timezone.now()
                              time_difference = date2 - date1
                              difference_in_seconds = time_difference.total_seconds()
                              if difference_in_seconds > 5:
                                   status = "valid"
                              else:
                                   status = "invalid"
                    else:
                         status = "valid"
                    
                    if status == 'valid':
                        remaining = float(curbalance)-float(cashout)
                        totalcout = float(tlcashout)+float(cashout)
                        if remaining>=0:
                           remainWalbal = remaining
                           
                           try:
                              curbalance = float(curbalance)
                              cashout = float(cashout)
                              remaining = float(remaining)
                              totalcout = float(totalcout)
                              
                           except ValueError:
                              newBalance = remainWalbal
                              data = 'error'
                    
                           try:
                              user_profile = UserProfile.objects.get(id=request.user.id)
                           except UserProfile.DoesNotExist:
                              newBalance = remainWalbal
                              data = 'error'
                              
                           pwallet.w_balance=remainWalbal
                           pwallet.wallet_out=totalcout
                           pwallet.save()  
                              
                           transaction = UWalletCashout(
                           cw_player=user_profile,
                           cw_bal=curbalance,
                           cw_out=cashout,
                           cw_remaining=remaining,
                           cw_code=code_cashout,
                           cw_agentid=agentid
                           )
                           transaction.save()
                           newBalance = remainWalbal
                           newtotalout = totalcout
                           data = 'ok'
                        else:
                           newBalance = curbalance
                           data = 'invalid'
                    else:
                         newBalance = curbalance
                         data = 'tryagain'
               else:
                    newBalance = curbalance
                    data = 'insufficient'
        else:
             newBalance = curbalance 
             data = 'invalid'
    return JsonResponse({'data': data, 'newPoints':newBalance, 'newtotalout':newtotalout})   


@login_required(login_url='/')
def loadCashOutTbl(request):
    hwallet = UWalletCashout.objects.filter(cw_player=request.user).order_by('-cw_created')
    context={
          'page':'WALLET',
          'transactions': hwallet
     }
    html_content = render_to_string('ugs_app/homepage/load_cashout_table.html', context)
    return HttpResponse(html_content)













@csrf_exempt
def setlongwin(request):
    fid = request.POST.get('fight')
    winner = request.POST.get('winner')
    gameid = request.POST.get('gameid')
    fightnum = int(request.POST.get('fightnum', 0))

    try:
        longwinner = Longestfight.objects.filter(
            l_status='WAITING', 
            l_category='LONGEST'
        ).aggregate(total=Sum('l_amount'))['total'] or 0

        countlong = Longestfight.objects.filter(
            l_status='WAITING', 
            l_category='LONGEST'
        ).aggregate(total=Count('id'))['total'] or 0

        if longwinner > 0 and countlong > 0:
            longDivide = longwinner / countlong
            lbets = Longestfight.objects.filter(
                l_won_amnt=0, 
                l_status='WAITING',
                l_fightno__lte=fightnum
            )

            if not lbets.exists():
                raise ValueError("No bets found for this fight")

            with transaction.atomic():
                for lbet in lbets:
                    if longDivide > 0:
                        lbet.l_won_amnt = longDivide
                        lbet.l_status = 'CLAIMED'
                        lbet.save()

                        try:
                            clwallet = UserWallet.objects.get(user=lbet.l_player.id)
                            clwallet.w_balance += longDivide
                            clwallet.w_betlong += longDivide
                            clwallet.save()
                            data = 'ok'
                   
                        except UserWallet.DoesNotExist:
                            data = 'bad'
                          
                    else:
                        data = 'bad'
                    #     print('longDivide <= 0')
        else:
            data = 'bad'
    except Exception as e:
        data = 'bad'

    return JsonResponse({'data': data})


@login_required(login_url='/')
def adstaking(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'SUPER ADMIN':
         adstakelist = Stakefund.objects.all().order_by('-s_id')
         users=UserProfile.objects.all().order_by('-date_joined')

         context = {
            'page': 'staking',
            'adstakelist': adstakelist,
            'users':list(users)
        }
         return render(request, 'ugs_app/homepage/admin_staking.html', context)
    else:
         return redirect(reverse('homepage'))
    


@csrf_exempt
def loadStaking(request):
    if request.method == 'POST':
        code_point = get_random_string(12)
        code_stake = code_point.upper()
        stakeamnt = request.POST.get('valstakeamnt')
        user_id = request.POST.get('userId')

        try:
            stakeamnt = Decimal(stakeamnt)
        except (ValueError, TypeError):
            return JsonResponse({'data': 'error1'})

        try:
            receiver = UserProfile.objects.get(id=user_id)
            sender = UserProfile.objects.get(id=request.user.id)
        except UserProfile.DoesNotExist:
            return JsonResponse({'data': 'error2'})

        try:
            with transaction.atomic():
                stakefund = Stakefund.objects.create(
                    s_code=code_stake,
                    s_amount=stakeamnt,
                    s_user=receiver,
                    s_sender=sender
                )
                
                stkwallet = UserWallet.objects.get(user=receiver.id)
                stkwallet.w_stakebal += stakeamnt
                stkwallet.save()

            data = 'ok'
        except Exception as e:
            data = 'error'

        return JsonResponse({'data': data})

    return JsonResponse({'data': 'error3'})



@login_required(login_url='/')
def load_stake_tbl(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'SUPER ADMIN':
          adstakelist = Stakefund.objects.all().order_by('-s_id')
          users=UserProfile.objects.all().order_by('-date_joined')
          context = {
            'page': 'staking',
            'adstakelist': adstakelist,
            'users':list(users)
        }
          html_content = render_to_string('ugs_app/homepage/load_stake_tbl.html', context)
          return HttpResponse(html_content)
    else:
         return redirect(reverse('homepage'))



@login_required(login_url='/')
def userwallet(request):
     agent=UserAccount.objects.get(user=request.user.id)
     hwallet = UWalletCashout.objects.filter(cw_player=request.user.id).order_by('-cw_id')
     context={
          'page':'WALLET',
          'transactions': hwallet,
          'agent': agent,
     }
     return render(request, 'ugs_app/homepage/user_wallet.html', context)


@login_required(login_url='/')
def cashoutapproval(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'AGENT' or usertype_ss == 'SUPER ADMIN':
          couthwallet = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=0).select_related('cw_player').order_by('-cw_id')
          total_approved = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=1).aggregate(Sum('cw_out'))['cw_out__sum']
          total_declined = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=2).aggregate(Sum('cw_out'))['cw_out__sum']
          total_current = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=0).aggregate(Sum('cw_out'))['cw_out__sum']

          if total_approved is None:
               total_approved = 0
          if total_declined is None:
               total_declined = 0
          if total_current is None:
               total_current = 0
          context = {
               'page': 'CASHOUT APPROVAL',
               'couttransact': couthwallet,
               'total_approved': total_approved,
               'total_declined': total_declined,
               'total_current': total_current,
               }
          return render(request, 'ugs_app/homepage/cashout_approval.html', context)
    else:
       return redirect(reverse('homepage'))
    





@csrf_exempt
def coutapproval(request):
    usertype_ss = request.session.get('usertype')
    if usertype_ss == 'AGENT' or usertype_ss == 'SUPER ADMIN':
        if request.method == 'POST':
            coutstat = request.POST.get('coutstat')
            vcoutid = request.POST.get('vcoutid')
            coutstat = int(coutstat)
            reqbal = ""
            appbal = ""
            decbal = ""
            wallbal = ""
            try:
                cotwallet = UWalletCashout.objects.get(cw_code=vcoutid, cw_stat=0)
                cotwallet.cw_stat = coutstat
                cotwallet.cw_approved=request.user.id
                cotwallet.cw_appdate=timezone.now()
                cotwallet.save()

                agntwallet = UserWallet.objects.get(user=cotwallet.cw_agentid)
                wallbal = agntwallet.w_balance

                total_current = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=0).aggregate(Sum('cw_out'))['cw_out__sum']   
                total_approved = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=1).aggregate(Sum('cw_out'))['cw_out__sum']
                total_declined = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=2).aggregate(Sum('cw_out'))['cw_out__sum']
                if total_current is None:
                   total_current = 0
                if total_approved is None:
                   total_approved = 0
                if total_declined is None:
                   total_declined = 0
                reqbal = total_current
                appbal = total_approved
                decbal = total_declined
                
                if coutstat == 1:
                     agntwallet.w_balance += cotwallet.cw_out
                     agntwallet.agent_cOut += cotwallet.cw_out
                     agntwallet.save()
                     data = 'approved'
                     wallbal = agntwallet.w_balance
                elif coutstat == 2:
                     cawallet = UserWallet.objects.get(user=cotwallet.cw_player.id)
                     cawallet.w_balance += cotwallet.cw_out
                     cawallet.wallet_out -= cotwallet.cw_out
                     cawallet.save()
                     data = 'declined'
                else:
                     data = 'error'
            except UWalletCashout.DoesNotExist:
                data = 'bad'
            except Exception as e:
               data = 'bad'

            return JsonResponse({'data': data, 'bal': wallbal, 'reqbal': reqbal, 'appbal': appbal, 'decbal': decbal}) 
    else:
        return redirect(reverse('homepage'))
    




@login_required(login_url='/')
def loadagentcOut(request):
     usertype_ss = request.session.get('usertype')
     if usertype_ss == 'AGENT' or usertype_ss == 'SUPER ADMIN':
          couthwallet = UWalletCashout.objects.filter(cw_agentid=request.user.id, cw_stat=0).select_related('cw_player').order_by('-cw_id')
          context = {
               'page': 'CASHOUT APPROVAL',
               'couttransact': couthwallet,
               }
          html_content = render_to_string('ugs_app/homepage/load_agentcOut_table.html', context)
          return HttpResponse(html_content)
     else:
        return redirect(reverse('homepage'))






# @login_required(login_url='/')
# def appstaking(request):
#     usertype_ss = request.session.get('usertype')
#     if usertype_ss == 'PLAYER' or usertype_ss == 'AGENT':
#          user_id = request.user.id
#          adstakelist = Stakefund.objects.all().order_by('-s_id')
#          users=UserProfile.objects.all().order_by('-date_joined')

#          context = {
#             'page': 'staking',
#             'adstakelist': adstakelist,
#             'users':list(users)
#         }
#          return render(request, 'ugs_app/homepage/staking_player.html', context)
#     else:
#          return redirect(reverse('homepage'))
# ------------------mmmmmmmmm---------------------------