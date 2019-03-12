from django import forms
from .models import User, Tweet, UserProfileInfo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"), widget=forms.PasswordInput,
                                help_text=("Enter the same password as above, for verification."))
    bio = forms.CharField(label=("Tell us about yourself"), max_length=200)
    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'bio')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user