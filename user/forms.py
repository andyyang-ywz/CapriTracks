from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
   class Meta:
      model = User
      fields = ["username", "email", "password1", "password2"]

class LoginForm(forms.Form):
   email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={
      'class': 'w-full bg-transparent border border-slate-500 rounded-sm mt-1 p-2 text-[13px] md:text-sm outline-none'
   }))
   password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
      'class': 'w-full bg-transparent border border-slate-500 rounded-sm mt-1 p-2 text-[13px] md:text-sm outline-none'
   }))