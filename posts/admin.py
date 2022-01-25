from django.contrib import admin
from .models import Post, User


# Define User admin class.
class UserAdmin(admin.ModelAdmin):
    """
    define user admin.
    Request admin model.
    """
    list_display = ("name", "email", "password", "profile", "type", "phone", "address", "dob", "created_user_id", "updated_user_id", "deleted_user_id", "created_at", "updated_at", "deleted_at")

    fields = ["name", "email", "password", "profile", "type", "phone", "address", "dob", "profile"]

class PostAdmin(admin.ModelAdmin):
    """
    define post admin.
    Request admin model.
    """
    list_display = ("title", "description", "status", "created_user_id", "updated_user_id", "deleted_user_id", "created_at", "updated_at", "deleted_at")

    fields = ["title", "description", "status"]

class Password_ResetAdmin(admin.ModelAdmin):
    """
    define password rest admin.
    Request admin model.
    """
    list_display = ("email", "token", "created_at")

    fields = ["email", "token"]

# Register the models.
admin.site.register(Post)
admin.site.register(User)