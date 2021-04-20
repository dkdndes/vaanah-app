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

    #     if 'username' in [f.name for f in User._meta.fields]:
    #         user.username = self.cleaned_data['username']

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
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
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

    # def _authenticate(self, request, email=None, password=None, *args, **kwargs):
    #     if email is None:
    #         if 'username' not in kwargs or kwargs['username'] is None:
    #             return None
    #         clean_email = normalise_email(kwargs['username'])
    #     else:
    #         clean_email = normalise_email(email)

    #     # Check if we're dealing with an email address
    #     # if '@' not in clean_email:
    #     #     return None

    #     # Since Django doesn't enforce emails to be unique, we look for all
    #     # matching users and try to authenticate them all. Note that we
    #     # intentionally allow multiple users with the same email address
    #     # (has been a requirement in larger system deployments),
    #     # we just enforce that they don't share the same password.
    #     # We make a case-insensitive match when looking for emails.
    #     matching_users = User.objects.filter(email__iexact=clean_email)
    #     authenticated_users = [
    #         user for user in matching_users if (user.check_password(password) and self.user_can_authenticate(user))]
    #     if len(authenticated_users) == 1:
    #         # Happy path
    #         return authenticated_users[0]
    #     elif len(authenticated_users) > 1:
    #         # This is the problem scenario where we have multiple users with
    #         # the same email address AND password. We can't safely authenticate
    #         # either.
    #         raise User.MultipleObjectsReturned(
    #             "There are multiple users with the given email address and "
    #             "password")
    #     return None

    # def authenticate(self, *args, **kwargs):
    #     return self._authenticate(*args, **kwargs)
