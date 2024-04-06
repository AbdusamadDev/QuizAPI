from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models



class Teacher(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^\+?\d{1,20}$",
        message="Phone number must start with + and must not contain more than 20 digits.",
    )
    phonenumber = models.CharField(
        validators=[phone_regex], max_length=21, unique=True, default="+123456789"
    )
    state = models.BooleanField(default=False)
    fullname = models.CharField(max_length=100, default="...")