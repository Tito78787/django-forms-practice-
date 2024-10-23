from django.db import models
# Create your models here.
import datetime
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager



class Contact (models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=100)
    password = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.name} - {self.email}'

        
# class CustomUser(AbstractUser):
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',  message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('N', 'Prefer not to say')
]


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',  message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    