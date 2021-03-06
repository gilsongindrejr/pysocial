from django import forms

from dashboard.models import Post


class PostModelForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('image', 'comment')
