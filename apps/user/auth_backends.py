from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.validators import validate_email
from django.contrib.auth.forms import AuthenticationForm


user_model = get_user_model()

class AuthenticationEmailBackend(AuthenticationForm):
    def authenticate(self, request, uname=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        uname = forms.CharField(label=_("Email or username"), max_length=30)
        password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
        try:
            user = User.objects.get(email=uname)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(uname=uname)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def login(request,*args,**kwargs):
        form=UserLoginForm(request.POST or None)
        if form.is_valid():
            user_obj=form.cleaned_data.get('user_obj')
            print(user_obj)
            # username = user_obj['query']
            # password = user_obj['password']
            uname = user_obj.uname
            password = user_obj.password
            user = authenticate(uname=uname, password=password)
            if user is not None:
                print("in login")
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'login1.html',  {'form': form})
        return render(request, 'articles/login1.html',{'form':form})




   
    # def authenticate(self, request, username=None, password=None, **kwargs):
    #     if username is None:
    #         username = kwargs.get(user_model.USERNAME_FIELD)
    #     if username is None or password is None:
    #         return
    #     try:
    #         validate_email(username)
    #     except ValidationError as e:
    #         kwargs = {'username__iexact': username}  # remove __iexact to make it case sensitive
    #     else:
    #         kwargs = {'email__iexact': username}  # remove __iexact to make it case sensitive
    #     try:
    #         user = user_model.objects.get(**kwargs)
    #     except user_model.DoesNotExist:
    #         return None
    #     else:
    #         if user.check_password(password) and self.user_can_authenticate(user):
    #             return user

    # def get_user(self, user_id):
    #     try:
    #         return user_model.objects.get(pk=user_id)
    #     except user_model.DoesNotExist:
    #         return None