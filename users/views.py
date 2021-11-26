from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect

from .forms import UserCreationForm, UserChangeForm, FriendForm

from .models import Friendship


class FriendshipHandlerView(View):

    def get(self, request):
        form = FriendForm()

        # get friend requests received and sent
        requests_received = Friendship.objects.filter(friend__email=request.user.email)
        requests_sent = Friendship.objects.filter(user__email=request.user.email)

        # join all friend requests
        friend_requests = list(requests_received) + list(requests_sent)

        # create a list with all friend request with accepted == True
        friendships = [friendship for friendship in friend_requests if friendship.accepted]

        # iterate over requests received of the user to look for unaccepted friend requests
        # increment waiting_friend_requests on which friend request still unaccepted
        waiting_friend_requests = 0
        for f_request in requests_received:
            if not f_request.accepted:
                waiting_friend_requests += 1

        context = {
            'form': form,
            'requests_received': requests_received,
            'waiting_friend_requests': waiting_friend_requests,
            'friendships': friendships,
        }
        return render(request, 'users/friends.html', context)

    def post(self, request):
        context = {'form': FriendForm()}
        form_email = FriendForm(request.POST)

        # get friend requests received and sent
        requests_received = Friendship.objects.filter(friend__email=request.user.email)
        requests_sent = Friendship.objects.filter(user__email=request.user.email)
        context['requests_received'] = requests_received

        waiting_friend_requests = 0
        for f_request in requests_received:
            if not f_request.accepted:
                waiting_friend_requests += 1
        context['waiting_friend_requests'] = waiting_friend_requests

        friend_requests = list(requests_received) + list(requests_sent)

        # create a list with all friend request with accepted == True
        friendships = [friendship for friendship in friend_requests if friendship.accepted]
        context['friendships'] = friendships

        if form_email.is_valid():
            friend_email = form_email.cleaned_data['friend']
            # check if friend_email is in friend list by checking in who sent the request
            # and in from who the user received the request
            if friend_email in [friendship.user.email for friendship in friendships] or friend_email in [friendship.friend.email for friendship in friendships]:
                context['alert'] = 'Already in friend list!'
                return render(request, 'users/friends.html', context)
            # check if user has already sent friend request to friend_email
            if friend_email in [friendship.friend.email for friendship in requests_sent if friendship.accepted is not True]:
                context['alert'] = 'Already send friend request to this user!'
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


def remove_friend(request, email):
    friend = Friendship.objects.filter(user__email=email, friend__email=request.user.email)
    friend2 = Friendship.objects.filter(user__email=request.user.email, friend__email=email)
    friendship = list(friend) + list(friend2)
    friendship[0].delete()
    return redirect('users:friends')


class RegisterUserView(CreateView):
    template_name = 'users/register.html'
    model = get_user_model()
    # Still has to implement success url
    success_url = reverse_lazy('url_name')
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
