from django.urls import path, re_path
from . import views

urlpatterns = [
    path("posts/", views.index, name="index"),
    path("post/create/", views.post_create, name="post-create"),
    path("post/<int:pk>/update/", views.post_update, name="post-update"),
    path("post/delete/", views.post_delete, name="post-delete"),
    path("post/detail/", views.post_detail, name="post-detail"),
    path("users/", views.userList, name="user-list"),
    path("user/create/", views.user_create, name="user-create"),
    path("user/<int:pk>/update/", views.user_update, name="user-update"),
    path("user/detail/", views.user_detail, name="user-detail"),
    path("user/profile/", views.user_profile, name="user-profile"),
    path("user/delete/", views.user_delete, name="user-delete"),
    path("post/list/download/", views.download_post_list_csv, name="post-list-download"),
    path("csv/import/", views.csv_import, name="csv-import"),
    re_path(r"^accounts/login/$", views.user_login, name="user_login"),
    re_path(r"^accounts/register/$", views.signup, name="create_account")
]