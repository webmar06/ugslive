from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.http.request import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile,UserAccount,UserWallet,Games,Fight,Bet,Longestfight
from staking_app.models import *
# Register your models here.

class UserAccountLine(admin.StackedInline):
    model=UserAccount
    can_delete=False
    verbose_name_plural='useraccount'
    fk_name='user'

class UserWalletLine(admin.StackedInline):
    model=UserWallet
    can_delete=False
    verbose_name_plural='userwallet'
    fk_name='user'



class CustomUserAccountAdmin(UserAdmin):
    inlines=(UserAccountLine,UserWalletLine)

admin.site.register(Longestfight)
admin.site.register(Bet)
admin.site.register(Games)
admin.site.register(Fight)
admin.site.register(StakeLogs)
admin.site.register(StakeSlot)
admin.site.register(UserProfile, CustomUserAccountAdmin)