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


def get_requests_received(request):
    return Friendship.objects.filter(friend__email=request.user.email)


def get_requests_sent(request, email_only=False):
    friendships_obj = Friendship.objects.filter(user__email=request.user.email)
    if email_only:
        return [friendship.friend.email for friendship in friendships_obj]
    return friendships_obj


def get_friendships(request, email_only=False):
    friend_requests = list(get_requests_received(request)) + list(get_requests_sent(request))
    accepted_requests_obj = [friendship for friendship in friend_requests if friendship.accepted]
    if email_only:
        friends_sender = [friendship.user.email for friendship in accepted_requests_obj
                          if friendship.user.email != request.user.email]
        friends_receiver = [friendship.friend.email for friendship in accepted_requests_obj
                            if friendship.friend.email != request.user.email]
        return friends_receiver + friends_sender
    return accepted_requests_obj


def get_waiting_friend_requests(request):
    waiting_friend_requests = 0
    for f_request in get_requests_received(request):
        if not f_request.accepted:
            waiting_friend_requests += 1
    return waiting_friend_requests
