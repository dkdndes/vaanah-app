from django import views
from django.utils.translation import gettext_lazy as _

from oscar.apps.customer.views import AccountAuthView 
from .authentification import EmailOrUsernameModelBackend
from .auth_backends import AuthenticationEmailBackend

class AccountAuth(AccountAuthView):
  
    template_name = 'templates/oscar/customer/login_registration.html'
    login_form_class = AuthenticationEmailBackend
    redirect_field_name = 'next'
   
    def post(self, request, *args, **kwargs):
        # Use the name of the submit button to determine which form to validate
        if 'login_submit' in request.POST:
            return self.login()
        return http.HttpResponseBadRequest()

from oscar.apps.customer.views import *  # noqa isort:skip
def login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username_or_email, password=password)
        print(user)
        if user is not None:
            return reverse('task:home')
        else:
            messages.error(request, "Username or password is invalid")
            return render(request, 'accounts/login.html')
    else:
         return render(request, 'accounts/login.html')
