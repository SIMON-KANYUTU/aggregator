# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import Article
from .models import SavedArticle
from .models import Profile
from .forms import ProfileUpdateForm, CustomPasswordResetForm
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse
from django import forms


@csrf_protect
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Add a success message
            messages.success(request, 'Login successful.')
            return redirect('/')  # Redirect to the index page after login
        else:
            # Authentication failed, handle the error
            error_message = 'Authentication Failed. Please check your credentials.'
            return render(request, 'newsauth/register.html', {'error_message': error_message})

    return render(request, 'newsauth/register.html')


@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return render(request, 'newsauth/register.html', {'error_message': 'Username already in use. Please choose another username.'})
        email = request.POST.get('email')
        # Check if the email already exists in the database
        if User.objects.filter(email=email).exists():
            # Email already used, render registration form with error message
            return render(request, 'newsauth/register.html', {'error_message': 'Email already in use. Please choose another email.'})
        # Proceed with registration logic if email is not already used
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.create_user(username, email, password)
            if user is not None:
                login(request, user)
                # Add a success message
                messages.success(
                    request, 'You have been registered successfully!')
                # Redirect to the index page after signup
                return redirect('/')
            else:
                # Error creating the user, handle the error (e.g., display a message)
                error_message = 'Error creating the user.'
                return render(request, 'newsauth/register.html', {'error_message': error_message})

        else:
            # Passwords do not match, handle the error (e.g., display a message)
            error_message = 'Passwords do not match.'
            return render(request, 'newsauth/register.html', {'error_message': error_message})

    return render(request, 'newsauth/register.html')


def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to the index page after logout


@login_required
def save_article(request, article_id):
    # Get the article object based on the article_id
    article = Article.objects.get(pk=article_id)

    # Create a new SavedArticle instance
    article = SavedArticle.objects.create(
        user=request.user, article=article)

    # Redirect the user to a suitable page after saving the article
    # Redirect to the news list page or any other page
    messages.success(
        request, 'You have Saved this Article!')
    return redirect('saved_articles')


@login_required
def saved_articles(request):
    saved_articles = SavedArticle.objects.filter(user=request.user)
    return render(request, 'newsauth/saved_articles.html', {'saved_articles': saved_articles})


@login_required
def profile_update(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        # If the profile doesn't exist, create a new one
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to a success page or render a success message
            # Redirect to the same page after updating
            return redirect('profile_update')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'newsauth/profile_update.html', {'form': form, 'profile': profile})


def forgot_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password1']
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(
                request, 'Your password has been successfully reset.')
            return redirect('login')  # Redirect to login page
    else:
        form = CustomPasswordResetForm()
    return render(request, 'newsauth/forgot_password.html', {'form': form})
