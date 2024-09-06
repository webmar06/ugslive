from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.utils import timezone
import datetime,time
import uuid
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.core import serializers
from django.core.serializers import serialize
import json
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
from ugs_app.views import *
from staking_app.views import *
from staking_app.forms import *





def home_stake(request):
    games=Games.objects.filter(g_status='OPEN')
    context={
          'page':'STAKING',
           'stakeform':StakeForm(),
           'wallet':request.user.userwallet.w_balance
     }
    return render(request,'staking/index.html',context)



def save_stake(request):
    stake=StakeForm(request.POST)

    if stake.is_valid():
        slot = stake.save(commit = False)
        slot.user=request.user
        slot.s_name=request.POST.get('s_name')
        slot.s_rate=request.POST.get('s_rate')
        slot.s_amount=request.POST.get('s_amount')
        slot.save()

        data='form Valid'
    else:

        data='Invalid Form'
    return JsonResponse({'data':data})