from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _

from .manager import UserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''Custom user model'''

    username = models.CharField (unique=True, null=False, max_length=30)
    email = models.EmailField (_('email address'), unique=True, null=False)
    first_name = models.CharField(max_length=128, null=False, default='')
    last_name = models.CharField(max_length=128, null=False, default='')
    profile_pic = models.ImageField(default='profile_pics/default.PNG', upload_to='profile_pics', null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        related_name='custom_users'  # Add a unique related_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        related_name='custom_users'  # Add a unique related_name
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
