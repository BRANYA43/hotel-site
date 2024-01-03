import re
from typing import Literal

from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

from accounts.models import Profile

User = get_user_model()

NOT_MATCH_PASSWORDS_ERROR_MESSAGE = 'Password and Confirmed password must be match.'
SAVE_ERROR_MESSAGE = 'User could not be created because data did not validate.'
EXISTED_USER_ERROR_MESSAGE = 'User with such a email is existed.'


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        password = self.cleaned_data['password']
        self.instance.set_password(password)
        return super().save(commit)


class UserRegisterForm(forms.Form):
    email = forms.CharField(max_length=255, label='Електронна пошта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    confirmed_password = forms.CharField(widget=forms.PasswordInput, label='Підтвердження пароля')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exists():
            raise ValidationError(EXISTED_USER_ERROR_MESSAGE, code='existed_user')

        return email

    def clean_confirmed_password(self):
        password = self.cleaned_data.get('password')
        confirmed_password = self.cleaned_data.get('confirmed_password')

        if (password and confirmed_password) and (password != confirmed_password):
            raise ValidationError(NOT_MATCH_PASSWORDS_ERROR_MESSAGE, code='invalid_password')

    def save(self):
        if self.errors:
            raise ValueError(SAVE_ERROR_MESSAGE)
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = User.objects.create_user(email, password)

        return user


INVALID_CREDENTIAL_DATA_ERROR_MESSAGE = 'Invalid credential data. Please, enter a correct email and password.'
NOT_CONFIRMED_EMAIL_ERROR_MESSAGE = (
    'Your email is not confirmed. Please, check your email and follow instruction ' 'for confirming email.'
)


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=255, label='Електронна пошта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)

            if self.user_cache is None:
                raise ValidationError(INVALID_CREDENTIAL_DATA_ERROR_MESSAGE, code='invalid_credential_data')

            if not self.user_cache.email_is_confirmed:
                raise ValidationError(NOT_CONFIRMED_EMAIL_ERROR_MESSAGE, code='not_confirmed_email')

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


INVALID_TELEPHONE_ERROR_MESSAGE = (
    'Invalid telephone. Please, enter a correct telephone ' 'by this pattern 38 050 000 00 00 or 050 000 00 00.'
)
INVALID_NAME_ERROR_MESSAGE = 'Invalid {0} name. Please, enter a correct your {0} name, use only letters.'


class ProfileUpdateFormMixin(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birthday', 'telephone']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    @staticmethod
    def _clean_name(name: str, type: Literal['first', 'last']):
        if name and re.findall(r'[^a-zA-Zа-яА-ЯіІїЇєЄґҐ]', name):
            msg = INVALID_NAME_ERROR_MESSAGE.format(type)
            raise ValidationError(msg, code='invalid_name')

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        self._clean_name(name, 'first')
        return name

    def clean_last_name(self):
        name = self.cleaned_data.get('last_name')
        self._clean_name(name, 'last')
        return name

    def clean_telephone(self):
        tel = self.cleaned_data.get('telephone')

        if tel:
            tel = ''.join(re.findall(r'\d+', tel))
            len_ = len(tel)

            if len_ != 10 and len_ != 12:
                raise ValidationError(INVALID_TELEPHONE_ERROR_MESSAGE, code='invalid_telephone')

            if len_ == 12:
                tel = tel[2:]

        return f'+38 ({tel[:3]}) {tel[3:6]} {tel[6:8]} {tel[8:10]}'


class UserRegisterContinueForm(ProfileUpdateFormMixin):
    class Meta(ProfileUpdateFormMixin.Meta):
        pass


class UserAccountForm(ProfileUpdateFormMixin):
    class Meta(ProfileUpdateFormMixin.Meta):
        pass
