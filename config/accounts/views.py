from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_http_methods
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создать профиль для пользователя
            Profile.objects.create(user=user)
            # Логинить пользователя после регистрации
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required(login_url='login')
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile_obj.phone = request.POST.get('phone', '')
        profile_obj.city = request.POST.get('city', '')
        profile_obj.address = request.POST.get('address', '')
        profile_obj.save()
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'profile': profile_obj})

@login_required(login_url='login')
def my_orders(request):
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})
