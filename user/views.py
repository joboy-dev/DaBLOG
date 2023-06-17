from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from user.models import CustomUser

# Register User Functionality
class RegisterView(View):

    def get(self, request):
        return render(request, 'user/register.html', {'title':'Register'})

    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        context = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'confirmpassword': request.POST.get('confirm-password'),
            'password': request.POST.get('password'),
        }

        # Passwords check
        if password == confirm_password:
            # Email exist check
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return render(request, 'user/register.html', context)
                
            # Username exist check
            elif CustomUser.objects.filter(username=username).exists():
                messages.info(request, f"Username '{username}' already taken")
                return render(request, 'user/register.html', context)
            
            elif len(username) < 6:
                messages.info(request, "Username must contain 6 or more characters")
                return render(request, 'user/register.html', context)
            
            elif len(password) < 8 or len(confirm_password) < 8:
                messages.info(request, "Password must contain 8 or more characters")
                return render(request, 'user/register.html', context)
            
            # Pass check
            else:
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
                user.save()

                messages.success(request, f'Account created for {username}. Login now')
                return redirect(reverse_lazy('user:login'))
        
        else:
            messages.error(request, 'Your passwords do not match') 
            return render(request, 'user/register.html', context)


# Login functionality
class LoginV(View):

    def get(self, request):
        return render(request, 'user/login.html', {'title':'Login',})
        
    def post(self, request):
        success_url = reverse_lazy('blog:home')

        username = request.POST['username']
        password = request.POST['password']
        
        context = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
        }

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {username}')
            return redirect(success_url)
        else:
            messages.error(request, 'Invalid Credentials. Check your username or password')
            
            return render(request, 'user/login.html', context)

        

class UserDetails(LoginRequiredMixin, View):

    login_url = 'user:login'

    def get(self, request):
        return render(request, 'user/profile.html', {'title':'My Profile'})
    

class GetUserDetails(LoginRequiredMixin, DetailView):

    login_url = 'user:login'

    model = CustomUser
    template_name = 'blog/home.html'
    context_object_name = 'user-details'

    def get(self, request):
        users = self.model.objects.all()


class UpdateUserProfile(LoginRequiredMixin, UpdateView):

    login_url = 'user:login'

    model = CustomUser
    fields = ['username', 'email']
    template_name = 'user/profile-update.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('user:user-details')

    def post(self, request, pk):
        current_user = self.request.user
        user_queryset = self.model.objects.get(pk=pk)

        username = request.POST['username']
        email = request.POST['email']

        # Email exist check
        if self.model.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists')
            
        # Username exist check
        elif self.model.objects.filter(username=username).exists():
            messages.info(request, f"Username '{username}' already taken")
        
        elif len(username) < 6:
            messages.info(request, "Username must contain 6 or more characters")

        else:
            user_queryset.username = username
            user_queryset.email = email

            if current_user == user_queryset:
                user_queryset.save()
                messages.success(request, 'Profile updated successfully')
                # return redirect(self.success_url)
            else:
                messages.error(request, 'You cannot update a profile that is not yours')
        
        return redirect(self.success_url)
        

class UploadProfilePicture(LoginRequiredMixin, UpdateView):

    login_url = 'user:login'

    model = CustomUser
    fields = ['profile_pic']
    template_name = 'user/profile-update.html'
    success_url = reverse_lazy('user:user-details')

    def post(self, request, pk):
        current_user = self.request.user
        user_queryset = self.model.objects.get(pk=pk)

        user_queryset.profile_pic = request.FILES.get('profile-pic')

        if current_user == user_queryset:
            user_queryset.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(self.success_url)
        else:
            messages.error(request, 'You cannot update a profile that is not yours')
            return redirect(self.success_url)

def logout_view(request):
    logout_url = reverse('user:login')

    current_user = request.user
    logout(request)

    messages.success(request, f'Goodbye, {current_user}')
    return redirect(logout_url)
