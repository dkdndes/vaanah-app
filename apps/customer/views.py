from django import views

from django.utils.translation import gettext_lazy as _

from oscar.apps.customer.views import AccountAuthView 
from apps.customer.forms import EmailAuthenticationForm
from django.http import HttpResponseRedirect


class AccountAuth(AccountAuthView):
    def login(request):
        if request.method == 'POST':
            login_form_class = EmailAuthenticationForm(request.POST)
            if login_form_class.is_valid():
                cd = login_form_class.cleaned_data
                if '@' in username:
                    user = authenticate(username=cd['email'], password=cd['password'])
                else:
                    user = authenticate(username=cd['uname'], password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/dashboard/')
                    else:
                        return HttpResponse('Disabled account')

                else:
                    return HttpResponse('Invalid login')
            else:
                login_form_class = EmailAuthenticationForm()

            return render(request, 'templates/oscar/customer/login_registration.html', {'login_form_class': login_form_class})
