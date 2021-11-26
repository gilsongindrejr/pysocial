from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from stdimage import StdImageField
from django.contrib.auth import get_user_model


def get_file_path(_instance=None, filename=None) -> str:
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return f'users/{filename}'


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField('email', max_length=50, unique=True)
    first_name = models.CharField(_('first name'), max_length=20, blank=False)
    last_name = models.CharField(_('last name'), max_length=20)
    image = StdImageField(_('image'), upload_to=get_file_path, variations={'thumb': (480, 480)}, default='', blank=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    def __str__(self):
        return self.email

    objects = UserManager()


class Friendship(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(get_user_model(), verbose_name=_('user'), related_name='user', on_delete=models.CASCADE)
    friend = models.ForeignKey(get_user_model(), verbose_name=_('friend'), related_name='friends', on_delete=models.CASCADE)
    accepted = models.BooleanField(_('accepted'), default=False)

    def __str__(self):
        return f'Friendship between {self.user.email} and {self.friend.email}'
