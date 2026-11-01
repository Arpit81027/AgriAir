from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from core.forms import FarmerRegistrationForm
from core.models import FarmerProfile


def register(request):
    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            FarmerProfile.objects.create(
                user=user,
                farm_name=form.cleaned_data['farm_name'] or f'{user.username.title()} Farm',
                district=form.cleaned_data['city'] or 'Not set',
                state=form.cleaned_data['state'],
                city=form.cleaned_data['city'],
                soil_type=form.cleaned_data['soil_type'],
                crop_type='Wheat',
                acreage=0,
            )
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome to AgriAir!')
            return redirect('dashboard')
    else:
        form = FarmerRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    form.fields['username'].widget.attrs.update({
        'placeholder': 'Enter your username',
        'autocomplete': 'username',
        'autofocus': True,
    })
    form.fields['password'].widget.attrs.update({
        'placeholder': 'Enter your password',
        'autocomplete': 'current-password',
    })
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
