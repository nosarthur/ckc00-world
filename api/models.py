from django.db import models
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class Tag(models.Model):
    """
    Many2Many with MyUser
    """
    name = models.CharField(max_length=32, primary_key=True,)

    def __str__(self):
        return self.name


class Division(models.Model):
    """
    This is the class each user belongs to.
    """
    name = models.CharField(max_length=16, unique=True,)
    number = models.CharField(max_length=1, unique=True,)

    class Meta:
        unique_together = ('name', 'number')


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        if not password:  # zombie user created by admin
            password = self.make_random_password()
            extra_fields['is_active'] = False
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    A custom class for user authentication. It gets rid of 'username' and uses
    'email' for that purpose.
    """
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    # required fields
    email = models.EmailField(max_length=64, unique=True,)
    first_name = models.CharField(max_length=20,)
    last_name = models.CharField(max_length=20, )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    # optional fields
    employer = models.CharField(max_length=64, blank=True, default='')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17,
        blank=True, default='')
    division = models.ForeignKey('Division', on_delete=models.SET_NULL,
        blank=True, null=True)
    homepage = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    # bookkeeping fields
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL,
        blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True,)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


