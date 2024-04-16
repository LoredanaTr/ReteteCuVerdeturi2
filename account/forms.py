from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# in acest fisier vom crea clasele necesare pt a defini formulare personalizate
class RegisterForm(UserCreationForm): # aici am definit o clasa cu ajutorul caruia putem gestiona formularul pt register
    class Meta: # aceasta clasa ne ajuta sa definim metadatele formularului
        model = User
        fields = ('username', 'email', 'password1', 'password2') #acestea sunt campurile pe care formularul le va contine

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'row gy-4'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'row gy-4'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'row gy-4'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'row gy-4'
    }))