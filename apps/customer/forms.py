from django import forms
from django.utils.translation import gettext_lazy as _

from oscar.apps.customer.forms import UserForm as CoreUserForm, EmailUserCreationForm as CoreEmailUserCreationForm
from oscar.apps.customer.forms import EmailAuthenticationForm
from oscar.core.compat import (existing_user_fields, get_user_model)
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()


class UserForm(CoreUserForm):
    class Meta:
        model = User
        fields = CoreUserForm.Meta.fields + existing_user_fields(['uname', 'gender', 'country', 'city', 'street','recovery_email',])

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password1'])

    #     if 'uname' in [f.name for f in User._meta.fields]:
    #         user.uname = self.cleaned_data['uname']

    #     if commit:
    #         user.save()
    #     return user

ProfileForm = UserForm

class EmailUserCreationForm(CoreEmailUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','type_user','uname','gender', 'country', 'city', 'street','recovery_email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if 'uname' in [f.name for f in User._meta.fields]:
            user.uname = self.cleaned_data['uname']

        if commit:
            user.save()
        return user



class EmailOrUsernameModelBackend(AuthenticationForm):
    def _authenticate(self, request, email=None, password=None, *args, **kwargs):
        if '@' in uname:
            kwargs = {'email': uname}
        else:
            kwargs = {'uname': uname}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


