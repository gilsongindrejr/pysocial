from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import  Paginator

from dashboard.models import Post
from dashboard.forms import PostModelForm

from users.models import get_friendships


def order_post_by_creation(post):
    return post.created


class DashboardView(View, LoginRequiredMixin):

    def get(self, request):
        form = PostModelForm()
        friends = get_friendships(request, email_only=True)
        user_posts = Post.objects.filter(author__email=request.user.email)
        friends_posts = []
        for friend in friends:
            friends_posts += Post.objects.filter(author__email=friend)
        posts = list(user_posts) + friends_posts

        # order posts by creation date
        posts.sort(reverse=True, key=order_post_by_creation)

        # pagination
        paginator = Paginator(posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'form': form,
            'friends': friends,
            'page_obj': page_obj,
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