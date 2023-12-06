from django import forms
from django.contrib.auth import get_user_model

from apps.registration.exceptions import RegistrationValidationError

ERROR_MESSAGE_USERNAME_LESS_THAN_3 = 'Username should be more than 2'
ERROR_MESSAGE_PASSWORDS_DO_NOT_EQUALLY = 'Passwords should be equal'
ERROR_MESSAGE_PASSWORD_LESS_THAN_7 = 'Passwords should be >= 8'

User = get_user_model()


class RegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self) -> str:
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise RegistrationValidationError(
                ERROR_MESSAGE_USERNAME_LESS_THAN_3,
            )
        return username

    def clean_password2(self) -> str:
        cd = self.cleaned_data
        password = cd['password']

        if password != cd['password2']:
            raise RegistrationValidationError(
                ERROR_MESSAGE_PASSWORDS_DO_NOT_EQUALLY,
            )

        if len(password) < 8:
            raise RegistrationValidationError(
                ERROR_MESSAGE_PASSWORD_LESS_THAN_7,
            )

        return password
