from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    '''Custom base user manager'''

    def create_user(self, username, password, **extras):
        '''Function to create regular user'''

        # check if username field is empty
        if not username:
            raise ValueError(_('Username field cannot be empty'))

        # create user instance
        user = self.model(username=username, **extras)

        # set user password
        user.set_password(password)

        # save user instance and return it
        user.save()
        return user
    
    def create_superuser(self, username, password, **extras):
        '''Function to create superuser'''

        extras.setdefault('is_active', True)
        extras.setdefault('is_staff', True)
        extras.setdefault('is_superuser', True)

         # check if is_staff and is_superuser is True
        if extras.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_admin=True'))

        if extras.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        
        # create user
        user = self.create_user(username=username, password=password, **extras)

        return user