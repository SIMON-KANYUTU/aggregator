from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for email and username
        self.fields['email'].initial = self.instance.user.email
        self.fields['username'].initial = self.instance.user.username

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.user.pk).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def save(self, commit=True):
        user = self.instance.user
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.save()
        return super().save(commit)


class CustomPasswordResetForm(PasswordResetForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(
        label='Confirm new password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(
                "The two password fields didn't match.")
        return cleaned_data
