from datetime import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class MyAccountManager(BaseUserManager):
    def create_user(self, fullname, phonenumber, password=None):
        if not fullname:
            raise ValueError('User must have an fullname')
        
        if not phonenumber:
            raise ValueError('User must have an phonenumber')
        
        user = self.model(
            fullname = fullname,
            phonenumber = phonenumber,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, fullname, phonenumber, password):
        user = self.create_user(
            fullname = fullname,
            phonenumber = phonenumber,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Teacher(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^\+?\d{1,20}$",
        message="Phone number must start with + and must not contain more than 20 digits.",
    )

    fullname = models.CharField(max_length=100, default="...")
    phonenumber = models.CharField(
        validators=[phone_regex], max_length=21, unique=True, default="+123456789"
    )

    # required
    date_joined    = models.DateTimeField(default=datetime.now)
    last_login     = models.DateTimeField(default=datetime.now)
    is_admin       = models.BooleanField(default=False)
    is_staff       = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=False)
    is_superadmin  = models.BooleanField(default=False)
    state = models.BooleanField(default=False)

    USERNAME_FIELD = "phonenumber"
    REQUIRED_FIELDS = ['fullname']

    objects = MyAccountManager()

    def __str__(self):
        return self.phonenumber
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_lable):
        return self.is_admin