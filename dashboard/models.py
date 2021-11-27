from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from stdimage import StdImageField
from django.utils.translation import gettext_lazy as _


def get_file_path(_instance=None, filename=None) -> str:
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return f'posts/{filename}'


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), related_name='author', verbose_name=_('author'), null=False, on_delete=models.CASCADE)
    created = models.DateTimeField(_('created'), auto_now_add=True, editable=False)
    image = StdImageField(_('image'), upload_to=get_file_path, null=False)
    comment = models.TextField(_('comment'), null=True)
