from django import views
from django.utils.translation import gettext_lazy as _

from oscar.apps.customer.views import AccountAuthView as CustomAccountAuthView
from .forms import CustomEmailAuthenticationForm

class AccountAuthView:
  
    login_form_class = CustomEmailAuthenticationForm
   


from oscar.apps.customer.views import *  # noqa isort:skip
