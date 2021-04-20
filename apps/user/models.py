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

    COSTUMER, SELLER = (
         'Customer', 'Seller', )
    TYPE_CHOICES = (
        (COSTUMER, 'Customer'),
        (SELLER, 'Seller'),
    )

    country        = models.CharField(default="Senegal",max_length=235)
    city        = models.CharField(default="Dakar",max_length=235)
    street        = models.CharField(default="Yoff",max_length=235)
    uname        = models.CharField(max_length=235,default='')
    recovery_email = models.EmailField() 

    type_user = models.CharField(max_length=20,
                              choices=TYPE_CHOICES, default=COSTUMER)
    gender = models.CharField(max_length=20,
                              choices=GENDER_CHOICES, default=MR)

 