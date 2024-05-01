from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.urls import reverse
from .models import UserAccount

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@admin_required
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if username and password:
            UserAccount.objects.create_user(username=username, password=password, role=role)
            messages.success(request, 'User registered successfully!')
            return redirect(reverse('login'))
        else:
            return JsonResponse({'success': False, 'message': 'Registration Failed.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect(reverse('admin_management'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@admin_required
def admin_management(request):
    users = UserAccount.objects.all()
    for user in users:
        print(user.username)
    return render(request, 'admin_management.html', {'users': users})

@admin_required
def modify_account(request, user_id):
    try:
        user = UserAccount.objects.get(id=user_id)
        user.username = request.POST.get('username')
        user.role = request.POST.get('role')
        user.is_active = request.POST.get('is_active')
        print(user.username, user.role, user.is_active)
        user.save()
        print(user.username, user.role, user.is_active)
        return redirect(reverse('admin_management'))
    except UserAccount.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User does not exist.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect(reverse("login"))
