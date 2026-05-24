from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserRegisterForm
from .models import Profile
from courses.models import Course, Favorite, Completed

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Аккаунт {user.username} создан! Теперь вы можете войти.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    Profile.objects.get_or_create(user=request.user)
    favorite_courses = Course.objects.filter(favorite__user=request.user)
    completed_courses = Course.objects.filter(completed__user=request.user)
    context = {
        'user': request.user,
        'favorite_courses': favorite_courses,
        'completed_courses': completed_courses,
    }
    return render(request, 'users/profile.html', context)