from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, firstname=None, lastname=None, contact_number=None, organisation=None, profession=None, gender='notsay',viewpass=None,password=None, ):
        if not email:
            raise ValueError("enter email")

        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            contact_number=contact_number,
            organisation=organisation,
            profession = profession,
            gender =gender,
            viewpass=viewpass,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, contact_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            # firstname=name,
            contact_number=contact_number,
            # viewpass=viewpass,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


GENDER_CHOICES = (
    ('male','Male'),
    ('female', 'Female'),
    ('notsay','Rather not say'),
)

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    viewpass = models.CharField(max_length=30, null=True, blank=True)
    firstname = models.CharField(max_length=20, null=True, blank=True)
    lastname = models.CharField(max_length=20, null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True)
    organisation = models.CharField(max_length=30, null=True, blank=True)
    profession = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default='notsay')
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact_number',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_admin

