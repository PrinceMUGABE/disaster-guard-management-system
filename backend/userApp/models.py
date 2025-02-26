from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self,first_name, last_name, phone_number, email, role, password=None):
        if not phone_number:
            raise ValueError("The phone number must be provided")
        if not email:
            raise ValueError("The email address must be provided")
        if not role:
            raise ValueError("The role must be provided")

        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, phone_number, email, password=None):
        """
        Creates and returns a superuser with admin role, setting is_staff and is_superuser to True.
        """
        # Set the role explicitly as 'admin' for superusers
        user = self.create_user(first_name, last_name, phone_number, email, role='admin', password=password)
        
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)  # Automatically set to the current date and time

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']  # Only require email for superuser creation

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
