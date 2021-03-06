from email.policy import default
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    """
    Creates and saves a User with the given email and password.
    """
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    """
    Creates and saves a staff user with the given email and password.
    """
    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user

    """
    Creates and saves a superuser with the given email and password.
    """
    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """Model representing User."""
    username = None
    name =models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True
    )
    password = models.CharField(max_length=255)
    profile = models.FileField(upload_to="", null=True, verbose_name="", default="/user_default.png")
    USER_TYPE = (
        ("0", "Admin"),
        ("1", "User")
    )

    type = models.CharField(
        max_length=1,
        choices=USER_TYPE,
        blank=True,
        default="u",
        help_text="User Type",
    )
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    created_user_id = models.IntegerField(default=1)
    updated_user_id = models.IntegerField(default=1)
    deleted_user_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
    deleted_at = models.DateField(null=True, blank=True)

    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] # Email & Password are required by default.
    objects = UserManager()

    def __str__(self):
        """return email to get auth data."""
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class Post(models.Model):
    """Model representing Post."""
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.IntegerField(default=1)
    created_user_id = models.IntegerField(default=1)
    updated_user_id = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    deleted_user_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
    deleted_at = models.DateField(null=True, blank=True)

    """String for representing the Model object."""
    def __str__(self):
        return self.title
    """Returns the url to access post list page."""
    def get_absolute_url(self):
        return reverse("index")