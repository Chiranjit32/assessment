# Create your models here.

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.utils.timezone import now


class UsersManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.deleted = False
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    pswd_token = models.CharField(max_length=255)
    is_login = models.IntegerField(null=True)
    last_login = models.DateTimeField(null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    deleted = models.IntegerField(default=False)
    created = models.DateTimeField(default=now)
    modified = models.DateTimeField(default=now)

    objects = UsersManager()

    EMAIL_FIELD = 'email'

    USERNAME_FIELD = 'username'

    # REQUIRED_FIELDS = ['username']

    class Meta:
        managed = True
        db_table = 'users'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class IPmodel(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    start_ip = models.CharField(max_length=39, blank=True, null=True)
    end_ip = models.CharField(max_length=39, blank=True, null=True)

class IpDayCount(models.Model):
    day = models.DateField()
    count = models.IntegerField(default=0)