
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpform(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Obrigatório. 150 caracteres ou menos. Letras, dígitos e @ /. / + / - / _ apenas.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=255, help_text='Obrigatório. Informe um endereço de e-mail válido.')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1','password2']
