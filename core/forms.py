from django import forms
from django.contrib.auth.models import User


class CreateUserForm(forms.Form):
        required_css_class = 'required'
        username = forms.CharField(max_length=30, label="Username")
        password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
        password2 = forms.CharField(widget=forms.PasswordInput, label="Password (again)")
        bio = forms.CharField(label="Tell us about yourself", max_length=200)
        profile_pic = forms.ImageField(label="Profile Picture")

        def clean_username(self):
            existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
            if existing.exists():
                raise forms.ValidationError("A user with that username already exists.")
            else:
                return self.cleaned_data['username']

        def clean_email(self):
            if User.objects.filter(email__iexact=self.cleaned_data['email']):
                raise forms.ValidationError(
                    "This email address is already in use. Please supply a different email address.")
            return self.cleaned_data['email']

        def clean(self):
            if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
                if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                    raise forms.ValidationError("The two password fields didn't match.")
            return self.cleaned_data

