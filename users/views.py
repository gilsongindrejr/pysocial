from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector

from .forms import UserCreationForm, UserChangeForm, SearchPeopleForm, SearchFriendForm

from .models import Friendship, get_requests_received, get_friendships, get_requests_sent, get_waiting_friend_requests


class FriendshipHandlerView(View):

    def get(self, request):

        context = {
            'search_people_form': SearchPeopleForm(),
            'requests_received': list(get_requests_received(request)),
            'requests_sent': get_requests_sent(request, email_only=True),
            'waiting_friend_requests': get_waiting_friend_requests(request),
            'friendships_email': get_friendships(request, email_only=True),
            'friendships': get_friendships(request),
            'search_friend_form': SearchFriendForm(),
        }

        if request.GET.get('search_friend'):
            form = SearchFriendForm(request.GET)
            if form.is_valid():
                search = form.cleaned_data['search_friend']
                raw_results = Friendship.objects.annotate(
                    search=SearchVector('friend__first_name', 'friend__last_name')
                ).filter(search=search)
                filtered_results = []
                for friendship in raw_results:
                    if friendship.accepted:
                        if friendship.user.email == request.user.email or friendship.friend.email == request.user.email:
                            filtered_results.append(friendship)
                context['search_friend'] = filtered_results

        if request.GET.get('search_people'):
            form = SearchPeopleForm(request.GET)
            if form.is_valid():
                search = form.cleaned_data['search_people']
                user_model = get_user_model()
                results = user_model.objects.annotate(
                    search=SearchVector('first_name', 'last_name')
                ).filter(search=search)
                context['search_people'] = results
        return render(request, 'users/friends.html', context)


def send_friend_request(request, pk):
    friend = get_object_or_404(get_user_model(), pk=pk)
    fs = Friendship()
    fs.user = request.user
    fs.friend = friend
    fs.save()
    return redirect('users:friends')


def accept_friendship(request, pk):
    fs = Friendship.objects.get(pk=pk)
    fs.accepted = True
    fs.save()
    return redirect('users:friends')


def deny_friendship(request, pk):
    fs = Friendship.objects.get(pk=pk)
    fs.delete()
    return redirect('users:friends')


def remove_friend(request, pk):
    fs = Friendship.objects.filter(id=pk)
    fs.delete()
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
