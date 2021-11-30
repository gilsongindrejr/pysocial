from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect

from .forms import UserCreationForm, UserChangeForm, FriendForm, SearchFriendForm

from .models import Friendship, get_requests_received, get_friendships, get_requests_sent, get_waiting_friend_requests


class FriendshipHandlerView(View):

    def get(self, request):

        context = {
            'form': FriendForm(),
            'requests_received': list(get_requests_received(request)),
            'waiting_friend_requests': get_waiting_friend_requests(request),
            'friendships': get_friendships(request),
            'search_form': SearchFriendForm(),
        }
        if request.GET.get('search'):
            form = SearchFriendForm(request.GET)
            if form.is_valid():
                email = form.cleaned_data['search']
                friends = get_friendships(request, email_only=True)
                if email in friends:
                    context['search'] = email
        return render(request, 'users/friends.html', context)

    def post(self, request):
        context = {}
        add_friend_form = FriendForm(request.POST)

        context = {
            'form': FriendForm(),
            'requests_received': get_requests_received(request),
            'waiting_friend_requests': get_waiting_friend_requests(request),
            'friendships': get_friendships(request),
            'search_form': SearchFriendForm(),
        }

        if add_friend_form.is_valid():
            friend_email = add_friend_form.cleaned_data['friend']

            # check if friend_email is in friend list by checking in who sent the request
            # and in from who the user received the request
            if friend_email in get_friendships(request, email_only=True):
                context['alert'] = 'Already in friend list!'
                return render(request, 'users/friends.html', context)
            # check if user has already sent friend request to friend_email
            if friend_email in get_requests_sent(request, email_only=True):
                context['alert'] = 'Already send friend request to this user!'
                return render(request, 'users/friends.html', context)
            if friend_email == request.user.email:
                context['alert'] = "That's your email!"
                return render(request, 'users/friends.html', context)

            friend = get_object_or_404(get_user_model(), email=friend_email)
            friendship = Friendship()
            friendship.user = request.user
            friendship.friend = friend
            friendship.save()
            context['alert'] = 'Request sent!'
        return render(request, 'users/friends.html', context)


def accept_friendship(request, pk):
    fd = Friendship.objects.get(pk=pk)
    fd.accepted = True
    fd.save()
    return redirect('users:friends')


def deny_friendship(request, pk):
    fd = Friendship.objects.get(pk=pk)
    fd.delete()
    return redirect('users:friends')


def remove_friend(request, pk):
    friendship = Friendship.objects.filter(id=pk)
    friendship.delete()
    return redirect('users:friends')


class RegisterUserView(CreateView):
    template_name = 'users/register.html'
    model = get_user_model()
    success_url = reverse_lazy('users:login')
    form_class = UserCreationForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'


class UpdateProfileView(LoginRequiredMixin, View):

    def get(self, request):
        form = UserChangeForm(instance=request.user)
        context = {'form': form}
        return render(request, 'users/update_profile.html', context)

    def post(self, request):
        form = UserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return render(request, 'users/profile.html')


class LoginView(LoginView):
    template_name = 'users/login.html'


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'users/logout.html'


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
