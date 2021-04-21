
import logging
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

import string    
import random

from oscar.apps.customer.signals import user_registered
from oscar.core.compat import get_user_model
from oscar.core.loading import get_class, get_model
from oscar.apps.customer.mixins import RegisterUserMixin as CoreRegisterUserMixin
from account.utils import Util

User = get_user_model()
Partner = get_model('partner', 'Partner')
CommunicationEventType = get_model('communication', 'CommunicationEventType')
CustomerDispatcher = get_class('customer.utils', 'CustomerDispatcher')

logger = logging.getLogger('oscar.customer')

class RegisterUserMixin(CoreRegisterUserMixin):

    def link_user(self, user, partner):
        """
        Links a user to a partner, and adds the dashboard permission if needed.

        Returns False if the user was linked already; True otherwise.
        """
        # if partner.users.filter(pk=user.pk).exists():
        #     return False
        partner.users.add(user)
        if not user.is_staff:
            dashboard_access_perm = Permission.objects.get(
                codename='dashboard_access',
                content_type__app_label='partner')
            user.user_permissions.add(dashboard_access_perm)
        return True

    def randomCode(self):
        S = 10  # number of characters in the string.  
        # call random.choices() string module to find the string in Uppercase + numeric data.  
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
        return str(ran)      

    def register_user(self, form):
        """
        Create a user instance and send a new registration email (if configured
        to).
        """
        user = form.save()
        user.is_active = False
        user.save()
        token = RefreshToken.for_user(user)
        current_site = get_current_site(self.request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.first_name+' Use link below to verify your email \n '+absurl
        data = {'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email'}
        Util.send_email(data)
        #self.send_registration_email(user)
        # print('==============================',user.is_active)
        # user = get_object_or_404(User, pk=user_pk)
        # name = user.get_full_name() or user.email
        if user.type_user =="Seller":
            partner = Partner.objects.create(code=self.randomCode(),name=user.first_name)
            if self.link_user(user, partner):
                messages.success(
                    self.request,'')
            else:
                messages.info(
                    self.request,'user is already linked to a partner')
        # return redirect('dashboard:partner-manage', pk=partner_pk)
        messages.info(
                    self.request,' Please check you email to activate your account before login')
        return user