from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth import authenticate, login
from accounts.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import SignupForm


class UserProfile(DetailView):
    model = Profile
    template_name = 'profile/profile.html'


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile/profile_form.html'
    fields = ['image', 'shop']

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.object.pk})


def delete_user(request, username):
    context = {}
    try:
        u = User.objects.get(username=username)
        u.delete()
        context['msg'] = 'The user is deleted.'
    except User.DoesNotExist:
        context['msg'] = 'User does not exist.'
    except Exception as e:
        context['msg'] = e.message
    return render(request, 'auth/user_confirm_delete.html', context=context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form':form})
