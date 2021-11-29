from django.contrib import admin
from django.contrib.auth import get_user_model

from dashboard.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment', 'image', 'created')
    list_filter = ('created',)
    ordering = ('created',)
    search_fields = ('comment', 'created')
    date_hierarchy = 'created'
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request, **kwargs):
        super(PostAdmin, self).get_queryset(request, **kwargs)
        return Post.objects.filter(author=request.user)
