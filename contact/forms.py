# type: ignore
# flake8: noqa

from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Escreva seu nome aqui'
            }
        ),
        label='Primero nome',
        # help_text='Texto de ajuda para seu usuário'

    )

    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ),
        required=False
    )

    class Meta:
        model = models.Contact
        fields = ('first_name',
                  'last_name',
                  'phone',
                  'email',
                  'description',
                  'category',
                  'picture',
                  )

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name_ = cleaned_data.get('first_name')
        last_name_ = cleaned_data.get('last_name')

        if first_name_ == last_name_:
            msg = ValidationError(
                'Primeiro nome não pode ser igual ao segundo',
                code='invalid'
            )
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        return super().clean()

    def clean_first_name(self):
        first_name_ = self.cleaned_data.get('first_name')

        if first_name_ == 'ABC':
            print('Passei no clean do first name')
            self.add_error(
                'first_name',
                ValidationError(
                    'Mensagem de erro',
                    code='invalid'
                )
            )

        return first_name_

# Classe para criar um usuário (user/crate)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True
    )
    last_name = forms.CharField(
        required=True
    )
    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        )

    # Criei a função para não cadastrarem emails repetidos
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Já existe este email', code='invalid')
            )

        return email

# Classe para atualizar o user (user/update)


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='*Obrigatório',
        error_messages={
            'min_length': 'Por favor, adicione mais de 2 caracteres.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='*Obrigatório',
    )
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label="Senha 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use a mesma senha anterior',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
        )

    # Salvando a senha na base
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    # Validar se os password1 é igual ao password2

    def clean(self):
        password1_ = self.cleaned_data.get('password1')
        password2_ = self.cleaned_data.get('password2')

        if password1_ or password2_:
            if password1_ != password2_:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )
        return super().clean()

    # Criei a função para não cadastrarem emails repetidos
    def clean_email(self):
        email_ = self.cleaned_data.get('email')
        print(f'Email que eu peguei na user/update {email_}')
        current_email = self.instance.email
        print(f'Email que eu peguei no instance da user/update {email_}')

        if current_email != email_:
            if User.objects.filter(email=email_).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este email', code='invalid')
                )

        return email_

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1
