from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy

from .forms import SignUpForm, UserEditForm, CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required


@login_required  # Ensure only logged-in users can access this view
def user_profile(request):
    user = request.user
    context = {
        'email': user.email,
        'username': user.username
    }
    return render(request, 'user/user_profile.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse_lazy("user:profile"))
    else:
        form = SignUpForm()
    return render(request, 'user/signup_template.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            return HttpResponseRedirect(reverse_lazy("user:profile"))
    else:
        user_form = UserEditForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'user/edit_profile.html', {'user_form': user_form, 'password_form': password_form})
