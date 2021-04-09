from django.db import models

from oscar.apps.customer.abstract_models import AbstractUser 

class User(AbstractUser):
    MR, MRS, OTHER = (
        'Mr', 'Mrs', 'Other', )
    GENDER_CHOICES = (
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (OTHER, 'Other'),
    )

    country        = models.CharField(default="Senegal",max_length=235)
    city        = models.CharField(default="Dakar",max_length=235)
    street        = models.CharField(default="Yoff",max_length=235)
    username        = models.CharField(max_length=235,default='')
    recovery_email = models.EmailField() 

    gender = models.CharField(max_length=20,
                              choices=GENDER_CHOICES, default=MR)

# USERNAME_FIELD = 'username'
# EMAIL_FIELD = 'email'