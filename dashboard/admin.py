from django.contrib import admin

from dashboard.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment', 'image', 'created')
    list_filter = ('created',)
    ordering = ('created',)
    search_fields = ('comment', 'created')
    date_hierarchy = 'created'

    def get_queryset(self, request, **kwargs):
        super(PostAdmin, self).get_queryset(request, **kwargs)
        return Post.objects.filter(author=request.user)
