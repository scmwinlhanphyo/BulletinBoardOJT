import datetime

from django import forms
from django.forms import ModelForm

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordResetForm

from posts.models import Users

class SeachPostForm(forms.Form):
    keyword = forms.CharField(
        required=False, label="keyword:", widget=forms.TextInput(attrs={'class': "form-control"}))

class SearchUserForm(forms.Form):
    name = forms.CharField(
        required=False, label="Name :", widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(
        required=False, label="Email :", widget=forms.EmailInput(attrs={'class': "form-control"}))
    from_date = forms.DateField(
        required=False, label="From :", widget=forms.DateInput(attrs={'class': "form-control", 'type': 'date'}))
    to_date = forms.DateField(
        required=False, label="To :", widget=forms.DateInput(attrs={'class': "form-control", 'type': 'date'}))

class PostForm(forms.Form):
    title = forms.CharField(
        required=False, label="Title *", widget=forms.TextInput(attrs={'class': "form-control"}))
    description = forms.CharField(
        required=False, label="Description *", widget=forms.Textarea(attrs={'class': "form-control"}))
    status = forms.BooleanField(
        required=False, label="Status *", widget=forms.CheckboxInput(attrs={'class': "form-control", 'name': 'status'}))
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'operation': 'edit'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/posts')

        return render(request, self.template_name, {'form': form, 'operation': 'edit'})

    def clean(self):
        if not self.cleaned_data.get('title'):
            self.add_error("title", "Title can't be blank")
        if not self.cleaned_data.get('description'):
            self.add_error("description", "Description can't be blank")
        if self.cleaned_data.get('description'):
            des = self.cleaned_data.get('description')
            if len(des) > 255:
                self.add_error("description", "255 characters is maximum allowed.")

class UserForm(forms.Form):
    name = forms.CharField(
        required=True, label="Name *", widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(
        required=True, label="E-Mail Address *", widget=forms.EmailInput(attrs={'class': "form-control"}))
    password = forms.CharField(
        required=True, label="Password *", widget=forms.TextInput(attrs={'class': "form-control", 'type': 'password'}))
    password_confirmation = forms.CharField(
        required=True, label="Password confirmation *", widget=forms.TextInput(attrs={'class': "form-control", 'type': 'password'}))
    USER_TYPE = (
        ('a', 'Admin'),
        ('u', 'User')
    )
    type = forms.CharField(
        required=True, label="Phone", widget=forms.Select(choices= USER_TYPE, attrs={'class': "form-control"}))
    phone = forms.CharField(
        required=False, label="Phone", widget=forms.TextInput(attrs={'class': "form-control"}))

    dob = forms.DateField(
        required=False, label="Dob", widget=forms.DateInput(attrs={'class': "form-control", 'type': 'date'}))
    address = forms.CharField(
        required=True, label="Address", widget=forms.TextInput(attrs={'class': "form-control"}))
    profile = forms.FileField(required=False, label="profile", widget=forms.FileInput(attrs={'class': "form-control"}))
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'operation': 'edit'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/users')
        return render(request, self.template_name, {'form': form, 'operation': 'edit'})

    def clean(self):
        if not self.cleaned_data.get('name'):
            self.add_error("name", "Name can't be blank")
        if not self.cleaned_data.get('email'):
            self.add_error("email", "Email can't be blank")
        if not self.cleaned_data.get('password'):
            self.add_error("password", "Password can't be blank")
        if not self.cleaned_data.get('password_confirmation'):
            self.add_error("password_confirmation", "Password Confirmation can't be blank")
        if self.cleaned_data.get('password') and self.cleaned_data.get('password_confirmation'):
            if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirmation'):
                self.add_error(None, "Password Confirmation must be match.")
        if not self.cleaned_data.get('address'):
            self.add_error("address", "Address can't be blank")

class UserEditForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="Name *",
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    email = forms.EmailField(
        required=False,
        label="E-Mail Address *",
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    USER_TYPE = (
        ('0', 'Admin'),
        ('1', 'User')
    )
    type = forms.CharField(
        required=True, 
        label="Type",
        widget=forms.Select(choices=USER_TYPE, attrs={'class': "form-control"})
    )
    phone = forms.CharField(
        required=False,
        label="Phone",
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    dob = forms.DateField(
        required=False,
        label="Date of birth",
        widget=forms.DateInput(attrs={'class': "form-control", 'type': "date"})
    )
    address = forms.CharField(
        required=False,
        label="Address",
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    profile = forms.FileField(
        required=False,
        label="Profile",
        widget=forms.FileInput(
            attrs={'class': "form-control", 'required': False})
    )

    def clean(self):
        if not self.cleaned_data.get('name'):
            self.add_error("name", "Name can't be blank")
        if not self.cleaned_data.get('email'):
            self.add_error("email", "E-Mail can't be blank")
        if self.cleaned_data.get('password') and self.cleaned_data.get('passwordConfirm'):
            if self.cleaned_data.get('password') != self.cleaned_data.get('passwordConfirm'):
                self.add_error(
                    None, "password and password confirmation must be match.")
        if not self.cleaned_data.get('address'):
            self.add_error("address", "Address can't be blank")

class SignUpForm(forms.Form):
    name = forms.CharField(
        required=True, label="Name *", widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(
        required=True, label="E-Mail Address *", widget=forms.EmailInput(attrs={'class': "form-control"}))
    password = forms.CharField(
        required=True, label="Password *", widget=forms.TextInput(attrs={'class': "form-control", 'type': 'password'}))
    password_confirmation = forms.CharField(
        required=True, label="Password confirmation *", widget=forms.TextInput(attrs={'class': "form-control", 'type': 'password'}))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/posts')
        return render(request, self.template_name, {'form': form})

    def clean(self):
        if not self.cleaned_data.get('name'):
            self.add_error("name", "Name can't be blank")
        if not self.cleaned_data.get('email'):
            self.add_error("email", "Email can't be blank")
        if not self.cleaned_data.get('password'):
            self.add_error("password", "Password can't be blank")
        if not self.cleaned_data.get('password_confirmation'):
            self.add_error("password_confirmation", "Password Confirmation can't be blank")
        if self.cleaned_data.get('password') and self.cleaned_data.get('password_confirmation'):
            if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirmation'):
                self.add_error(None, "Password Confirmation must be match.")

class CSVForm(forms.Form):
    csv_file = forms.FileField(required=False, label="CSV file", widget=forms.FileInput(attrs={'class': "form-control"}))

    def clean(self):
        if not self.cleaned_data.get('csv_file'):
            self.add_error("csv_file", "CSV File can't be blank")

class PasswordResetForm(forms.Form):
    password = forms.CharField(
        required=True, label="Current Password *", widget=forms.TextInput(attrs={'class': "form-control", 'type': 'password'}))
    new_password = forms.CharField(
        required=True, label="New Password *", widget=forms.TextInput(attrs={'class': "form-control", 'type': 'password'}))
    new_password_confirm = forms.CharField(
        required=True, label="New Confirm Password *", widget=forms.TextInput(attrs={'class': "form-control", 'type': 'password'}))

    def clean(self):
        if not self.cleaned_data.get('password'):
            self.add_error("name", "Password can't be blank")
        if not self.cleaned_data.get('new_password'):
            self.add_error("password", "New password can't be blank")
        if not self.cleaned_data.get('new_password_confirm'):
            self.add_error("new_password_confirm", "New confirm password can't be blank")
        if self.cleaned_data.get('password') and self.cleaned_data.get('password_confirmation'):
            if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirmation'):
                self.add_error(None, "News password and new password confirmation is not match.")

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        required=True, label="E mail*", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'email',
        'type': 'email',
        'name': 'email'
    }))