from django import forms
from django.utils.translation import gettext_lazy as _

from oscar.apps.customer.forms import UserForm as CoreUserForm,EmailUserCreationForm as CoreEmailUserCreationForm
from oscar.core.compat import (existing_user_fields, get_user_model)

User = get_user_model()


class UserForm(CoreUserForm):
    class Meta:
        model = User
        fields = CoreUserForm.Meta.fields + existing_user_fields(['address','recovery_email','username',])

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
        fields = ('email', 'first_name', 'last_name', 'address','recovery_email','username',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if 'username' in [f.name for f in User._meta.fields]:
            user.username = self.cleaned_data['username']

        if commit:
            user.save()
        return user

# ProfileForm = EmailUserCreationForm