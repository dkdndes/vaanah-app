
import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from oscar.apps.customer.signals import user_registered
from oscar.core.compat import get_user_model
from oscar.core.loading import get_class, get_model
from oscar.apps.customer.mixins import RegisterUserMixin as CoreRegisterUserMixin

User = get_user_model()
CommunicationEventType = get_model('communication', 'CommunicationEventType')
CustomerDispatcher = get_class('customer.utils', 'CustomerDispatcher')

logger = logging.getLogger('oscar.customer')

class RegisterUserMixin(CoreRegisterUserMixin):

    def register_user(self, form):
        """
        Create a user instance and send a new registration email (if configured
        to).
        """
        user = form.save()
        print('Hellloooooooooooooooooooooooooooooooooooo')

        return user