from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _ # noqa
from django.contrib.auth.models import User

from .models import AuthConfiguration


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('First name'),
        max_length=30,
        required=False,
    )
    last_name = forms.CharField(
        label=_('Last name'),
        max_length=30,
        required=False,
    )
    email = forms.EmailField(
        max_length=254,
        help_text=_('Required. Inform a valid e-mail address.'),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class AuthConfigurationForm(forms.ModelForm):
    class Meta:
        model = AuthConfiguration
        fields = ('auth_type', 'host', 'bind_dn', 'bind_password', 'user_search_base', 'user_filter', 'active')
