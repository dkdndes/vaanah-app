from django import forms
from django.utils.translation import gettext_lazy as _

from oscar.apps.customer.forms import UserForm as CoreUserForm, EmailUserCreationForm as CoreEmailUserCreationForm
from oscar.apps.customer.forms import EmailAuthenticationForm
from oscar.core.compat import (existing_user_fields, get_user_model)
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import get_user_model
from apps.customer.forms import EmailAuthenticationForm as CoreEmailUserCreationForm


# Login form customization



class EmailAuthenticationForm(CoreEmailUserCreationForm):
    username = forms.CharField(label=_("Email or username"))
    
   