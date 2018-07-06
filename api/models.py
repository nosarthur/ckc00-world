from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models


class CKCer(models.Model):
    user = models.OneToOneField(User)
    gender = models.BooleanField(blank=False)
    company = models.CharField(max_length=64, default=None)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
