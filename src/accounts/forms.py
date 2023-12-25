from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

User = get_user_model()

NOT_MATCH_PASSWORDS_ERROR_MESSAGE = 'Password and Confirmed password must be match.'
SAVE_ERROR_MESSAGE = 'User could not be created because data did not validate.'
EXISTED_USER_ERROR_MESSAGE = 'User with such a email is existed.'


class UserRegisterForm(forms.Form):
    email = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    confirmed_password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exists():
            raise ValidationError(EXISTED_USER_ERROR_MESSAGE, code='existed_user')

        return email

    def clean(self):
        password = self.cleaned_data.get('password')
        confirmed_password = self.cleaned_data.get('confirmed_password')

        if (password and confirmed_password) and (password != confirmed_password):
            raise ValidationError(NOT_MATCH_PASSWORDS_ERROR_MESSAGE, code='invalid_password')

        return super().clean()

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
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

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

            if not self.user_cache.is_confirmed_email:
                raise ValidationError(NOT_CONFIRMED_EMAIL_ERROR_MESSAGE, code='not_confirmed_email')

        return self.cleaned_data

    def get_user(self):
        return self.user_cache
