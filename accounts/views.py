from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.shortcuts import redirect, render

from .forms import ProfileForm, RegisterForm, UserUpdateForm
from .models import Profile
from django.core.mail import send_mail


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                subject='Welcome to DeepFocus',
                message=f'Hi {user.username}, your account is ready. Start your first focus session!',
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile_obj})


@login_required
def profile_edit(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'تم حفظ الملف الشخصي')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile_obj)
    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
