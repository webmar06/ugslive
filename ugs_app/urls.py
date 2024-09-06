
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

# from .views import load_new_user,load_points_table


urlpatterns = [
    # admin
    # path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('homepage',views.homepage,name='homepage'),
    path('registration/<str:code>',views.registration,name='registration'),
    path('upstat',views.upstat,name='upstat'),
    path('getusers',views.getusers,name='getusers'),
    path('admin-accounts',views.mydownlines,name='mydownlines'),
    
    # declarator
    path('decla_games',views.decla_games,name='decla_games'),
    path('load_games',views.load_games,name='load_games'),
    path('add_games',views.add_games,name='add_games'),
    path('update_games',views.update_games,name='update_games'),
    path('getgame',views.getgame,name='getgame'),
    path('gfight',views.gfight,name='gfight'),
    path('addfight',views.addfight,name='addfight'),
    path('decla/arena/<str:game_id>',views.decla_arena,name='decla_arena'),
    path('delgame',views.delgame,name='delgame'),

    # path('fight_stat',views.fight_stat,name='fight_stat'),
    # path('setwinner',views.setwinner,name='setwinner'),
    path('revert',views.revert,name='revert'),
    path('disburse',views.disburse,name='disburse'),
    path('nxtfight',views.nxtfight,name='nxtfight'),

    # PLAYER
    path('player_reg',views.player_reg,name='player_reg'),
   

    path('games',views.games,name='games'),
    path('setting',views.setting,name='setting'),
    path('users',views.users,name='users'),
    path('player/arena/<str:game_id>',views.arena,name='arena'),
    path('auth_user',views.auth_user,name='auth_user'),
    path('signout',views.signout,name='signout'),
    path('account_reg',views.account_reg,name='account_reg'),
    #betting
    path('lastcall',views.lastcall,name='lastcall'),
    path('closebet',views.closebet,name='closebet'),
    path('openbet',views.openbet,name='openbet'),
    path('updatewallet',views.updatewallet,name='updatewallet'),
    #settings
    path('uppass',views.uppass,name='uppass'),
    path('timer',views.timer,name='timer'),
    
    
    
    # -------mmmmmmmm-------------
    path('admin_points', views.admin_points, name='admin_points'),
    path('loadAdminPoints',views.loadAdminPoints,name='loadAdminPoints'),
    path('load_adpoints_table', views.load_adpoints_table, name='load_adpoints_table'),
    path('agentplayer',views.agentplayer,name='agentplayer'),
    path('upplyrstat',views.upplyrstat,name='upplyrstat'),
    path('load_new_user', views.load_new_user, name='load_new_user'),
    path('load_points', views.load_points, name='load_points'),
    path('loadAgentPoints',views.loadAgentPoints,name='loadAgentPoints'),
    path('load_points_table', views.load_points_table, name='load_points_table'),
    path('get-fight-data/', views.get_fight_data, name='get_fight_data'),
    path('fight_stat',views.fight_stat,name='fight_stat'),
    path('userwallet', views.userwallet, name='userwallet'),
    path('cashoutwallet', views.cashoutwallet, name='cashoutwallet'),
    path('loadCashOutTbl', views.loadCashOutTbl, name='loadCashOutTbl'),
    
    path('setwinner',views.setwinner,name='setwinner'),
    path('setlongwin',views.setlongwin,name='setlongwin'),
    path('adstaking',views.adstaking,name='adstaking'),
    path('loadStaking',views.loadStaking,name='loadStaking'),
    path('load_stake_tbl', views.load_stake_tbl, name='load_stake_tbl'),
    path('cashoutapproval', views.cashoutapproval, name='cashoutapproval'),
    path('coutapproval', views.coutapproval, name='coutapproval'),
    path('loadagentcOut', views.loadagentcOut, name='loadagentcOut'),
    # path('appstaking', views.appstaking, name='appstaking'),
    
    # ------mmmmmmmmm-------------- 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
