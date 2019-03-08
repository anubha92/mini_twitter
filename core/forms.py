from django import forms
from .models import UserProfileInfo, Tweet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('bio',)

class TweetsForm(forms.ModelForm):
    class Meta():
        model = Tweet
        fields=('contents',)