from django import forms
import django.forms.utils
import django.forms.widgets
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserAccount,UserWallet,Games,UserProfile,Fight,Points
from django.contrib.auth.password_validation import validate_password
from django.core import validators

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible

class LoginForm(forms.Form):
    
    username=forms.CharField(label="Username",max_length=50, widget=forms.TextInput(attrs={'autocomplete':'off','placeholder':'Username','class':'form-control mb-4 input-lg'}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control mb-4 input-lg '}))
   

class SignUpForm(forms.ModelForm):
    username=forms.CharField(label='Username',max_length=50, widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control '}))
    password = forms.CharField(max_length=50, widget = forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control pass1'}))
    confirm_password = forms.CharField(max_length=50, widget = forms.PasswordInput(attrs={'placeholder':' Confirmation','class':'form-control pass2'}))
    class Meta:
        model = UserProfile
        fields = ('username', 'password')

GENDER=(
    ('','SELECT GENDER'),
    ('MALE','MALE'),
    ('FEMALE','FEMALE')
)
USERTYPE=(
    ('','-------'),
    ('PLAYER','PLAYER'),
    ('AGENT','AGENT'),
    ('LOADER','LOADER'),
    ('DECLARATOR','DECLARATOR'),
    ('ADMIN','ADMIN'),
    ('FA','FA'),
)

WALLET_STATUS=(
    ('ACTIVE','ACTIVE'),
    ('ONHOLD','ONHOLD'),
    ('BANNED','BANNED'),
)
GAMES=(
    ('E-SABONG','E-SABONG'),
    ('BALL GAMES','BALL GAMES'),
    ('PERYA','PERYA'),
)

class UserForm(ModelForm):
    contact_no=forms.IntegerField(label='Contact', widget=forms.NumberInput(attrs={'minlength':'10','placeholder':'Mobile Number','class':'form-control'}))
    usertype=forms.ChoiceField(label='Account Type',widget=forms.Select(attrs={'class':'form-control bg-dark'}), choices=USERTYPE)
    class Meta:
        model = UserAccount
        fields=('contact_no',)

class WalletForm(ModelForm):
    w_balance=forms.IntegerField(label='Balance', widget=forms.NumberInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control'}))
    w_points=forms.IntegerField(label='Points', widget=forms.NumberInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control'}))
    w_commission=forms.IntegerField(label='Commission', widget=forms.NumberInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control'}))
    w_status=forms.ChoiceField(label='Status',widget=forms.Select(attrs={'class':'form-control '}), choices=WALLET_STATUS)
    class Meta:
        model = UserWallet
        fields=('w_balance','w_points','w_commission',)


class GameForm(ModelForm):
    
    g_name=forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder':'Title','class':'form-control'}))
    g_redname=forms.CharField(label='Meron Name', widget=forms.TextInput(attrs={'placeholder':'Red Side','class':'form-control'}))
    g_bluename=forms.CharField(label='Wala Name', widget=forms.TextInput(attrs={'placeholder':'Blue Side','class':'form-control'}))
    g_plasada=forms.DecimalField(label='Plasada',widget=forms.NumberInput(attrs={'placeholder':'Plasada','class':'form-control'}))
    g_desc=forms.CharField(label='Description', widget=forms.Textarea(attrs={'rows':'5','class':'form-control'}))
    g_category=forms.ChoiceField(label='Category',widget=forms.Select(attrs={'class':'form-control '}), choices=GAMES)
    g_image=forms.FileField(label='Event Image', widget=forms.FileInput(attrs={'class':'form-control'}))
    g_link=forms.CharField(label='Game Url', widget=forms.TextInput(attrs={'placeholder':'Url','class':'form-control'}))
    
    class Meta:
        model = Games
        fields=('g_name','g_redname','g_bluename','g_plasada','g_desc','g_category','g_link','g_image')

class FightForm(ModelForm):
    class Meta:
        model = Fight
        fields = "__all__"
        
        
class LoadPointsForm(forms.ModelForm):
    user_agent = forms.ModelChoiceField(
        queryset=UserAccount.objects.exclude(usertype='SUPER ADMIN').exclude(usertype='DECLARATOR'),
        label='Agent',
        to_field_name='user',
        widget=forms.Select(attrs={'id': 'agentid','class': 'form-control'})
    )
    load_amount = forms.IntegerField(
        label='Amount',
        widget=forms.NumberInput(attrs={'id': 'loadAmountField','maxlength': '2', 'placeholder': 'Points Amount', 'class': 'form-control','min':'1','step':'any'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_agent'].label_from_instance = self.label_from_user_account

    def label_from_user_account(self, user_account):
        return f'{user_account.user.username} - {user_account.user.first_name}'

    class Meta:
        model = Points
        fields = ('user_agent', 'load_amount')







class SendPoint(forms.ModelForm):
    user_agent = forms.ModelChoiceField(
        queryset=UserAccount.objects.exclude(usertype='SUPER ADMIN').exclude(usertype='DECLARATOR'),
        label='Agent',
        to_field_name='user',
        widget=forms.Select(attrs={'id': 'playerids','class': 'form-control'})
    )
    load_amount = forms.IntegerField(
        label='Amount',
        widget=forms.NumberInput(attrs={'id': 'loadAmount','maxlength': '2', 'placeholder': 'Points Amount', 'class': 'form-control','min':'1','step':'any'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_agent'].label_from_instance = self.label_from_user_account

    def label_from_user_account(self, user_account):
        return f'{user_account.user.username} - {user_account.user.first_name}'

    class Meta:
        model = Points
        fields = ('user_agent', 'load_amount')
