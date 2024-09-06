USE_TZ = False
TIME_ZONE = 'Asia/Shanghai'
from django.db import models
from django.db.models.deletion import RESTRICT,CASCADE
from django.contrib.auth.models import User,AbstractUser
import uuid
import datetime
from django.utils import timezone
from django.utils.translation import gettext as _
now= timezone.now
from django.conf import settings
now= timezone.now



class UserProfile(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
class UserAccount(models.Model):
    user=models.OneToOneField(UserProfile,on_delete=CASCADE,)
    contact_no=models.CharField(max_length=11,null=True, default='00000000000')
    relpass=models.CharField(max_length=50,null=True, blank=True)
    referral_code=models.CharField(max_length=200,null=True, blank=True)
    referral_link=models.CharField(max_length=200,null=True, blank=True)
    user_agent=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='agent')
    usertype=models.CharField(max_length=50,default='ADMIN', choices=[('SUPER ADMIN','SUPER ADMIN'),('ADMIN','ADMIN'),('DECLARATOR','DECLARATOR'),('LOADER','LOADER'),('AGENT','AGENT'),('PLAYER','PLAYER')]) 
    status=models.CharField(max_length=50,default='ACTIVE',choices=[('ACTIVE','ACTIVE'),('INACTIVE','INACTIVE'),('BANNED','BANNED')])
    
    def __str__(self):
        return str(self.user.username+' - '+self.usertype)
        
    def __str__(self):
        return str(self.user.username)

class UserWallet(models.Model):
    user=models.OneToOneField(UserProfile, on_delete=CASCADE)
    w_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    w_balance=models.IntegerField(default=0, blank=True)
    w_points=models.IntegerField(default=0, blank=True)
    w_betwins=models.IntegerField(default=0, blank=True)
    w_betlong=models.IntegerField(default=0, blank=True)
    w_commission=models.IntegerField(default=0, blank=True)
    w_stakebal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_stakecom = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_stakeuot = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_status=models.CharField(max_length=50,default='ACTIVE',choices=[('ACTIVE','ACTIVE'),('INACTIVE','INACTIVE'),('BANNED','BANNED')])
    w_dateupdate=models.DateTimeField(auto_now=True)
    commission_rate=models.DecimalField(default=0.00,max_digits=5, decimal_places=2)
    default_rate=models.DecimalField(default=0.00,max_digits=5, decimal_places=2)
    wallet_out=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    agent_cOut=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.user.username +' - '+str(self.w_id))
    
    


class Games(models.Model):
    g_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    g_name=models.CharField(max_length=50, blank=True)
    g_redname=models.CharField(max_length=50, blank=True)
    g_bluename=models.CharField(max_length=50, blank=True)
    g_plasada=models.DecimalField(default=0.00,max_digits=5, decimal_places=3)
    g_desc=models.CharField(max_length=100, blank=True)
    g_category=models.CharField(null=True,max_length=50,choices=[('E-SABONG','E-SABONG'),('BALL GAMES','BALL GAMES'),('PERYA','PERYA')])
    g_link=models.CharField(max_length=1000, blank=True)
    g_image=models.ImageField(blank=True, null=True ,upload_to='uploads/')
    g_status=models.CharField(default='CLOSED',max_length=50,choices=[('OPEN','OPEN'),('CLOSED','CLOSED')])
    g_by=models.CharField(max_length=100, blank=True)
    g_update=models.DateTimeField(auto_now=True)
    g_created=models.DateTimeField(default=timezone.now)
    g_col=models.IntegerField(default=1)

    class Meta:
       get_latest_by = ('-g_created',)

    def __str__(self):
        return str(self.g_name )


class Fight(models.Model):
    f_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    f_code=models.CharField(max_length=10,null=True, blank=True)
    f_number=models.IntegerField(blank=True,null=True)
    f_multiplier=models.DecimalField(default=0.00,max_digits=5, decimal_places=3)
    f_game=models.ForeignKey(Games,on_delete=CASCADE,related_name='game')
    f_winner=models.CharField(max_length=100,null=True, blank=True)
    f_longest=models.IntegerField(default=0)
    f_status=models.CharField(null=True,max_length=50,choices=[('OPEN','OPEN'),('CLOSED','CLOSED'),('CLOSING','CLOSING'),('DONE','DONE'),('LAST CALL','LAST CALL'),('DECLARED','DECLARED')])
    f_update=models.DateTimeField(auto_now=True)
    f_created=models.DateTimeField(auto_now_add=True)
    f_tblrows=models.IntegerField(default=0)

    class Meta:
        ordering = ['-f_created']

    def __str__(self):
        return str(str(self.f_game) +'- Winner:'+str(self.f_winner)+' ( Fight #: '+str(self.f_number)+' ) Status: '+str(self.f_status) )
    

class Bet(models.Model):
    id=models.AutoField(primary_key=True)
    player=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='player')
    fight=models.ForeignKey(Fight,default=uuid.uuid4,on_delete=CASCADE,related_name='fight')
    amount=models.IntegerField(blank=True)
    winning_amnt = models.CharField(max_length=50, default=0)
    won_amnt = models.CharField(max_length=100, default=0)
    winStat = models.CharField(max_length=100, default=0)
    category=models.CharField(null=True,max_length=50,choices=[('MERON','MERON'),('WALA','WALA'),('DRAW','DRAW'),('LONGEST','LONGEST')])
    status=models.CharField(default='PENDING',max_length=50,choices=[('PENDING','PENDING'),('WIN','WIN'),('LOSE','LOSE')])
    created=models.DateTimeField(auto_now_add=True)
    fightno = models.IntegerField(default=0)
    longest = models.IntegerField(default=0)
   
    def __str__(self):
        return str(str(self.player) + ' - '+ str(self.category)+' - '+str(self.amount)+' - '+str(self.fight) )
    
class Commission(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_fight = models.ForeignKey('Fight', on_delete=models.CASCADE, related_name='commissions')
    c_player = models.CharField(max_length=100)
    c_agent = models.CharField(max_length=100, default='')
    c_fnumber = models.CharField(max_length=50, default=0)
    c_betamnt = models.CharField(max_length=50)
    c_winner = models.CharField(max_length=50)
    c_commission = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Fight: {self.c_fight}, Player: {self.c_player}, Bet Amount: {self.c_betamnt}, Winner: {self.c_winner}, Commission: {self.c_commission}"
    
    
class Points(models.Model):
    p_id = models.AutoField(primary_key=True, editable=False)
    p_receiver = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE, related_name='p_userkey')
    p_sender = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE, related_name='p_headKey')
    p_code = models.CharField(blank=True, max_length=50, null=True)
    p_amount = models.CharField(blank=True, max_length=50, null=True)
    p_created = models.DateTimeField(auto_now_add=True)
    p_update = models.DateTimeField(auto_now=True)
    p_sellerUkey = models.CharField(null=True, max_length=100, blank=True)

    def __str__(self):
        return f'{self.p_receiver} - {self.p_code}'
    
class UWalletCashout(models.Model):
    cw_id = models.AutoField(primary_key=True)
    cw_code = models.CharField(blank=True, max_length=50, null=True)
    cw_player = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cw_player')
    cw_bal = models.DecimalField(max_digits=10, decimal_places=2)
    cw_out = models.DecimalField(max_digits=10, decimal_places=2)
    cw_remaining = models.DecimalField(max_digits=10, decimal_places=2)
    cw_update = models.DateTimeField(auto_now=True)
    cw_created = models.DateTimeField(auto_now_add=True)
    cw_agentid = models.CharField(blank=True, max_length=100, null=True)
    cw_stat = models.CharField(max_length=50, default=0)
    cw_approved = models.CharField(blank=True, max_length=100, null=True)
    cw_appdate = models.CharField(blank=True, max_length=20, null=True)
    
    def __str__(self):
        return f"Player: {self.cw_player}, Cashout: {self.cw_out}, Remaining: {self.cw_remaining}"
    

class Longestfight(models.Model):
    id=models.AutoField(primary_key=True)
    l_player=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='l_player')
    l_fight=models.ForeignKey(Fight,default=uuid.uuid4,on_delete=CASCADE,related_name='l_fight')
    l_amount=models.IntegerField(blank=True)
    l_won_amnt = models.CharField(max_length=100, default=0)
    l_category=models.CharField(null=True,max_length=50,choices=[('LONGEST','LONGEST')])
    l_status=models.CharField(default='WAITING',max_length=50,choices=[('WAITING','WAITING'),('CLAIMED','CLAIMED')])
    l_fightno = models.IntegerField(default=0)
    l_created=models.DateTimeField(auto_now_add=True)
    

class Stakefund(models.Model):
    s_id=models.AutoField(primary_key=True)
    s_code = models.CharField(blank=True, max_length=50, null=True)
    s_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    s_user = models.ForeignKey(UserProfile, related_name='stakefund_user', on_delete=models.CASCADE)
    s_sender = models.ForeignKey(UserProfile, related_name='stakefund_sender', on_delete=models.CASCADE)
    s_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stakefund {self.s_id} - Amount: {self.s_amount}"
    

    


       