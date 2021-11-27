from django.shortcuts import render, redirect
from django.views import View

from dashboard.models import Post
from dashboard.forms import PostModelForm

from users.views import get_friends


class DashboardView(View):

    def get(self, request):
        form = PostModelForm()
        friends = get_friends(request)
        user_posts = Post.objects.filter(author__email=request.user.email)
        friends_posts = []
        for friend in friends:
            friends_posts += Post.objects.filter(author__email=friend)
        posts = list(user_posts) + friends_posts
        posts.reverse()
        context = {
            'form': form,
            'friends': friends,
            'posts': posts,
        }
        return render(request, 'dashboard/dashboard.html', context)

    def post(self, request):
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post()
            post.author = request.user
            post.image = form.cleaned_data['image']
            post.comment = form.cleaned_data['comment']
            post.save()
            return redirect('dashboard:dashboard')
        return redirect('dashboard:dashboard')


def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('dashboard:dashboard')