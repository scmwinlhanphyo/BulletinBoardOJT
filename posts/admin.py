from django.contrib import admin
from .models import Posts, Password_Resets, Users


# Register your models here.
# Define the admin class
class UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password', 'profile', 'type', 'phone', 'address', 'dob', 'created_user_id', 'updated_user_id', 'deleted_user_id', 'created_at', 'updated_at', 'deleted_at')

    fields = ['name', 'email', 'password', 'profile', 'type', 'phone', 'address', 'dob', 'profile']

class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'created_user_id', 'updated_user_id', 'deleted_user_id', 'created_at', 'updated_at', 'deleted_at')

    fields = ['title', 'description', 'status']

class Password_ResetsAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created_at')

    fields = ['email', 'token']

admin.site.register(Posts)
admin.site.register(Password_Resets)
admin.site.register(Users)