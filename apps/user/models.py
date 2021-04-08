from django.db import models

from oscar.apps.customer.abstract_models import AbstractUser 

class User(AbstractUser):
    address        = models.CharField(max_length=235)
    username        = models.CharField(max_length=235,default='')
    recovery_email = models.EmailField() 


USERNAME_FIELD = 'username'
EMAIL_FIELD = 'email'