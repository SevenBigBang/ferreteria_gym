#new
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    first_name = forms.CharField(label='Nombres', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nombres'}))
    last_name = forms.CharField(label='Apellidos', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}))

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2']
        help_texts = {k: "" for k in fields }
        widgets = {
            'username': forms.TextInput(attrs={'maxlength': None, 'placeholder': 'Nombre de usuario'}),
        }

