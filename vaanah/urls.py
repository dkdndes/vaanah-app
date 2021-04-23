"""vaanah URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.apps import apps
from django.views.i18n import JavaScriptCatalog
from django.conf.urls.static import static

from django.conf import settings
from django.contrib.auth import views as auth_views

from apps.user import views

from apps.customer import views 
from account.views import VerifyEmail

#from apps import store_view 
#from boutique import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # from documantation site
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include(apps.get_app_config('oscar').urls[0])),
    # django-stores
    # adds URLs for the dashboard store manager
    path('dashboard/stores/', apps.get_app_config('stores_dashboard').urls),
    # adds URLs for overview and detail pages
    path('stores/', apps.get_app_config('stores').urls),
    # adds internationalization URLs
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    #path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    # adds internationalization URLs

    #Email verification
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),

    #password-reset urls
    path('', auth_views.PasswordResetCompleteView.as_view(template_name='communication/emails/password_reset_complete.html' ), name='commtype_password_reset_body'),

    #login
    #path('/accounts/login/', views.AuthenticationEmailBackend),
    #path('', views.AccountAuth.as_view()),

    #Partner store 
    #path('store/', store_view.StoreView)
    
 

    #Boutique
    path('dashboard/boutique/', apps.get_app_config('boutique_dashboard').urls),
    path('boutique/', apps.get_app_config('boutique').urls),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)