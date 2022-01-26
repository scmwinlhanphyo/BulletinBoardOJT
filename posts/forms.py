from django import forms
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponseRedirect
from posts.models import User

class SeachPostForm(forms.Form):
    """
    create search post form.
    Request django Form.
    """
    keyword = forms.CharField(
        required=False, label="keyword:", widget=forms.TextInput(attrs={"class": "form-control"}))

class SearchUserForm(forms.Form):
    """
    create search user form.
    Request django Form.
    """
    name = forms.CharField(
        required=False, label="Name :", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        required=False, label="Email :", widget=forms.EmailInput(attrs={"class": "form-control"}))
    from_date = forms.DateField(
        required=False, label="From :", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    to_date = forms.DateField(
        required=False, label="To :", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))

class PostForm(forms.Form):
    """
    create post form.
    Request django Form.
    """
    title = forms.CharField(
        required=False, label="Title *", widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(
        required=False, label="Description *", widget=forms.Textarea(attrs={"class": "form-control"}))
    status = forms.BooleanField(
        required=False, label="Status *", widget=forms.CheckboxInput(attrs={"class": "form-control", "name": "status"}))

    def clean(self):
        """check post form validation."""
        if not self.cleaned_data.get("title"):
            self.add_error("title", "Title can't be blank")
        if not self.cleaned_data.get("description"):
            self.add_error("description", "Description can't be blank")
        if self.cleaned_data.get("description"):
            des = self.cleaned_data.get("description")
            if len(des) > 255:
                self.add_error("description", "255 characters is maximum allowed.")

class UserForm(forms.Form):
    """
    create user form
    Request django Form.
    """
    name = forms.CharField(
        required=False, label="Name *", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        required=False, label="E-Mail Address *", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        required=False, label="Password *", widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))
    password_confirmation = forms.CharField(
        required=False, label="Password confirmation *", widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))
    USER_TYPE = (
        ("0", "Admin"),
        ("1", "User")
    )
    type = forms.CharField(
        required=False, label="Type", widget=forms.Select(choices= USER_TYPE, attrs={"class": "form-control"}))
    phone = forms.CharField(
        required=False, label="Phone", widget=forms.TextInput(attrs={"class": "form-control"}))

    dob = forms.DateField(
        required=False, label="Date of birth", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    address = forms.CharField(
        required=False, label="Address", widget=forms.TextInput(attrs={"class": "form-control"}))
    profile = forms.FileField(required=False, label="Profile *", widget=forms.FileInput(attrs={"class": "form-control"}))

    def clean(self):
        """check user form validation."""
        if not self.cleaned_data.get("name"):
            self.add_error("name", "Name can't be blank")
        if not self.cleaned_data.get("email"):
            self.add_error("email", "Email can't be blank")
        if not self.cleaned_data.get("type"):
            self.add_error("type", "Type can't be blank")
        if not self.cleaned_data.get("password"):
            self.add_error("password", "Password can't be blank")
        if not self.cleaned_data.get("password_confirmation"):
            self.add_error("password_confirmation", "Password Confirmation can't be blank")
        if self.cleaned_data.get("password") and self.cleaned_data.get("password_confirmation"):
            if self.cleaned_data.get("password") != self.cleaned_data.get("password_confirmation"):
                self.add_error(None, "Password Confirmation must be match.")
        if not self.cleaned_data.get("address"):
            self.add_error("address", "Address can't be blank")

class UserEditForm(forms.Form):
    """
    create user edit form.
    Request Django Form.
    """
    name = forms.CharField(
        required=False,
        label="Name *",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        required=False,
        label="E-Mail Address *",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    USER_TYPE = (
        ("0", "Admin"),
        ("1", "User")
    )
    type = forms.CharField(
        required=False, 
        label="Type",
        widget=forms.Select(choices=USER_TYPE, attrs={"class": "form-control"})
    )
    phone = forms.CharField(
        required=False,
        label="Phone",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    dob = forms.DateField(
        required=False,
        label="Date of birth",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    address = forms.CharField(
        required=False,
        label="Address",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    profile = forms.FileField(
        required=False,
        label="Profile",
        widget=forms.FileInput(
            attrs={"class": "form-control", "required": False})
    )

    def clean(self):
        """check user edit form validation."""
        if not self.cleaned_data.get("name"):
            self.add_error("name", "Name can't be blank")
        if not self.cleaned_data.get("email"):
            self.add_error("email", "E-Mail can't be blank")
        if not self.cleaned_data.get("address"):
            self.add_error("address", "Address can't be blank")

class SignUpForm(forms.Form):
    """
    create sign up form.
    Request Django Form.
    """
    name = forms.CharField(
        required=False, label="Name *", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        required=False, label="E-Mail Address *", widget=forms.EmailInput(attrs={"class": "form-control", "type": "email"}))
    password = forms.CharField(
        required=False, label="Password *", widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))
    password_confirmation = forms.CharField(
        required=False, label="Password confirmation *", widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))

    def clean(self):
        """signup form validation."""
        if not self.cleaned_data.get("name"):
            self.add_error("name", "Name can't be blank")
        if not self.cleaned_data.get("email"):
            self.add_error("email", "Email can't be blank")
        if not self.cleaned_data.get("password"):
            self.add_error("password", "Password can't be blank")
        if not self.cleaned_data.get("password_confirmation"):
            self.add_error("password_confirmation", "Password Confirmation can't be blank")
        if self.cleaned_data.get("password") and self.cleaned_data.get("password_confirmation"):
            if self.cleaned_data.get("password") != self.cleaned_data.get("password_confirmation"):
                self.add_error(None, "Password Confirmation must be match.")

class CSVForm(forms.Form):
    """
    create csv form.
    Request Django Form.
    """
    csv_file = forms.FileField(required=False, label="CSV file *", widget=forms.FileInput(attrs={"class": "form-control"}))

    """csv form validataion."""
    def clean(self):
        if not self.cleaned_data.get("csv_file"):
            self.add_error("csv_file", "CSV File can't be blank")

class PasswordResetForm(forms.Form):
    """
    create password reset form.
    Request Django Form.
    """
    password = forms.CharField(
        required=False, label="Current Password *", widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))
    new_password = forms.CharField(
        required=False, label="New Password *", widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))
    new_password_confirm = forms.CharField(
        required=False, label="New Confirm Password *", widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))

    def clean(self):
        """password reset form validataion"""
        if not self.cleaned_data.get("password"):
            self.add_error("password", "Password can't be blank")
        if not self.cleaned_data.get("new_password"):
            self.add_error("new_password", "New password can't be blank")
        if not self.cleaned_data.get("new_password_confirm"):
            self.add_error("new_password_confirm", "New confirm password can't be blank")
        if self.cleaned_data.get("new_password") and self.cleaned_data.get("new_password_confirm"):
            if self.cleaned_data.get("new_password") != self.cleaned_data.get("new_password_confirm"):
                self.add_error(None, "News password and new password confirmation is not match.")