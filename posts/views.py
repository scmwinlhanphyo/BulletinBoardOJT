from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.core import serializers
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from datetime import datetime
from posts.forms import PostForm, SearchUserForm, UserForm, UserEditForm, SignUpForm, CSVForm, PasswordResetForm, SeachPostForm
from posts.models import Post, User
from posts.helper import check_route, save_temp, handle_uploaded_file, remove_temp
import csv
import json


@login_required
def index(request):
    """
    View function for post list page of site.
    Param request user id
    Return post_list data and view.
    """
    post_list = []
    user = get_object_or_404(User, pk=request.user.id)
    form = SeachPostForm()
    query = Q()
    if user.type == "1":
        query.add(Q(created_user_id__exact=user.id), Q.AND)
    if (request.POST and request.POST["keyword"]):
        keyword = request.POST["keyword"]
        formData = {
            "keyword": keyword
        }
        form = SeachPostForm(initial=formData)
        query.add(Q(title__icontains=keyword), Q.OR)
        query.add(Q(description__icontains=keyword), Q.OR)

    query.add(Q(deleted_user_id=None), Q.AND)
    query.add(Q(deleted_at=None), Q.AND)
    post_list = Post.objects.filter(query)
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "form": form,
        "title": "Post List",
        "page_obj": page_obj
    }
    return render(request, "posts/post_list.html", context)


@login_required
def userList(request):
    """
    View function for user list page of site.
    Param request user id
    Return user_list data and view.
    """
    form = SearchUserForm()
    user = get_object_or_404(User, pk=request.user.id)
    print('---user list--%s' %request.user.id)
    query = Q()
    if user.type == "1":
        query.add(Q(created_user_id__exact=user.id), Q.AND)
    if (request.POST):
        print('--search user_list--------------------')
        # print(request)
        name = request.POST["name"]
        email = request.POST["email"]
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        formData = {
            "name": name,
            "email": email,
            "from_date": from_date,
            "to_date": to_date
        }
        form = SearchUserForm(initial=formData)
        if name:
            query.add(Q(name__icontains=name), Q.OR)
        if email:
            query.add(Q(email__icontains=email), Q.OR)
        if from_date:
            query.add(Q(created_at__gte=from_date), Q.AND)
        if to_date:
            query.add(Q(created_at__lte=to_date), Q.AND)

    query.add(Q(deleted_user_id=None), Q.AND)
    query.add(Q(deleted_at=None), Q.AND)

    user_list = User.objects.filter(query)

    for user_data in user_list:
        user_data.type = "Admin" if user_data.type == "0" else "User"
        list_data = User.objects.filter(id=user_data.created_user_id)
        user_data.created_user = list_data[0].email if len(
            list_data) > 0 else ""

    paginator = Paginator(user_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "form": form,
        "title": "User List",
        "page_obj": page_obj
    }
    return render(request, "posts/users_list.html", context)

def user_login(request):
    """
    View function for user login page of site.
    Param request user form data.
    Return login view.
    """
    login_username = ""
    form = AuthenticationForm()
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        email_user = User.objects.filter(
            email=email, deleted_user_id=None, deleted_at=None)
        if email_user:
            authUser = authenticate(request, username=email, password=password)
            if authUser:
                login(request, authUser)
                user = User.objects.get(email=email)
                if user.name and hasattr(user, "name"):
                    request.session["login_username"] = user.name
                else:
                    request.session["login_username"] = user.email
                login_username = user.name
                return redirect(request.POST.get("next", "/"))
            else:
                messages.info(request, f"Email and Password does not match.")
        else:
            messages.info(request, f"Email does not exist or deleted")
    return render(request, "registration/login.html", {"form": form, "title": "Login", "login_username": login_username})


@login_required
def post_create(request):
    """
    View function for post-create page of site.
    Param request post form data.
    Return post create view.
    """
    user = get_object_or_404(User, pk=request.user.id)
    formData = None
    form = PostForm()
    check_route("post", request.META.get("HTTP_REFERER"), request)
    if request.session.get("create_update_confirm_page_flag") is None:
        request.session["create_update_confirm_page_flag"] = False
    if request.method == "POST":
        if "_save" in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                if request.session["create_update_confirm_page_flag"] == True:
                    new_post = Post(
                        title=form.cleaned_data.get("title"),
                        description=form.cleaned_data.get("description"),
                        status="1",
                        user=user,
                        created_user_id=user.id,
                        updated_user_id=user.id,
                        created_at=timezone.now(),
                        updated_at=timezone.now()
                    )
                    new_post.save()
                    request.session["create_update_confirm_page_flag"] = False
                    return HttpResponseRedirect(reverse("index"))
                else:
                    formData = {
                        "title": form.cleaned_data.get("title"),
                        "description": form.cleaned_data.get("description")
                    }
                    form = PostForm(initial=formData)
                    request.session["create_update_confirm_page_flag"] = True
                    form.fields["title"].widget.attrs["readonly"] = True
                    form.fields["description"].widget.attrs["readonly"] = True
        else:
            request.session["create_update_confirm_page_flag"] = False
            return HttpResponseRedirect(reverse("post-create"))
    context = {
        "title": "Post Create",
        "form": form,
        "operation": "create",
        "create_update_confirm_page_flag": request.session["create_update_confirm_page_flag"]
    }
    return render(request, "posts/posts_form.html", context)


@login_required
def post_update(request, pk):
    """
    View function for post update page of site.
    Param request post form data.
    Return post update view.
    """
    user = get_object_or_404(User, pk=request.user.id)
    detail_post = get_object_or_404(Post, pk=pk)
    status = True if detail_post.status == 1 else False
    check_route("post", request.META.get("HTTP_REFERER"), request)
    form = PostForm(initial={"title": detail_post.title,
                    "description": detail_post.description,
                             "status": status})
    status = detail_post.status
    if request.session.get("create_update_confirm_page_flag") is None:
        request.session["create_update_confirm_page_flag"] = False
    if request.method == "POST":
        if "_save" in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                request.session["is_edit"] = True
                if request.session["create_update_confirm_page_flag"] == True:
                    status = 1 if request.session.get("status") == True else 0
                    edit_post = get_object_or_404(Post, pk=detail_post.id)
                    edit_post.title = form.cleaned_data.get("title")
                    edit_post.description = form.cleaned_data.get(
                        "description")
                    edit_post.status = status
                    edit_post.user = user
                    edit_post.updated_user_id = user.id
                    edit_post.updated_at = timezone.now()
                    edit_post.save()
                    request.session["create_update_confirm_page_flag"] = False
                    return HttpResponseRedirect(reverse("index"))
                else:
                    status = form.cleaned_data.get("status")
                    formData = {
                        "title": form.cleaned_data.get("title"),
                        "description": form.cleaned_data.get("description"),
                        "status": status
                    }
                    form = PostForm(initial=formData)
                    request.session["status"] = status
                    request.session["create_update_confirm_page_flag"] = True
                    form.fields["title"].widget.attrs["readonly"] = True
                    form.fields["description"].widget.attrs["readonly"] = True
                    form.fields["status"].widget.attrs["disabled"] = True
        else:
            request.session["create_update_confirm_page_flag"] = False
            return HttpResponseRedirect(reverse("post-update", kwargs={"pk": pk}))

    context = {
        "title": "Post Update",
        "detail_post": detail_post,
        "form": form,
        "operation": "edit",
        "create_update_confirm_page_flag": request.session["create_update_confirm_page_flag"]
    }
    return render(request, "posts/posts_form.html", context)


@login_required
def post_detail(request):
    """
    View function for post detail page of site.
    Param request post id.
    Return post detail view.
    """
    post_id = request.GET["post_id"]
    obj = Post.objects.get(pk=post_id)
    created_user_name = obj.user.email
    updated_user = User.objects.get(pk=obj.updated_user_id)
    data = serializers.serialize("json", [obj, ])
    struct = json.loads(data)
    struct[0]["created_user_name"] = created_user_name
    struct[0]["updated_user_name"] = updated_user.name
    data = json.dumps(struct[0])
    return HttpResponse(data)


@login_required
def user_detail(request):
    """
    View function for user detail page of site.
    Param request user id.
    Return user detail view.
    """
    user_id = request.GET["user_id"]
    obj = User.objects.get(pk=user_id)
    profile_url = ""
    if obj.profile and hasattr(obj.profile, "url"):
        profile_url = obj.profile.url
        profile_url = "media/" + profile_url.split("/")[-1]
    else:
        profile_url = "media/user-default.png"
    created_user = User.objects.get(
        pk=obj.created_user_id) if obj.created_user_id != None else None
    updated_user = User.objects.get(
        pk=obj.updated_user_id) if obj.updated_user_id != None else None
    data = serializers.serialize("json", [obj, ])
    struct = json.loads(data)
    struct[0]["created_user_name"] = created_user.email
    struct[0]["updated_user_name"] = updated_user.email
    struct[0]["profile"] = profile_url
    data = json.dumps(struct[0])
    return HttpResponse(data)


@login_required
def user_create(request):
    """
    View function for user create page of site.
    Param request user post form and file data.
    Return user create view.
    """
    form = UserForm()
    try:
        user = get_object_or_404(User, pk=request.user.id)
        formData = None
        check_route("user", request.META.get("HTTP_REFERER"), request)
        if request.session.get("create_update_confirm_page_flag") is None:
            request.session["create_update_confirm_page_flag"] = False

        if request.method == "POST":
            if "_save" in request.POST:
                form = UserForm(request.POST, request.FILES)
                if form.is_valid():
                    if request.session["create_update_confirm_page_flag"] == True:
                        handle_uploaded_file(request.session.get("profile"))
                        new_user = User(
                            name=form.cleaned_data.get("name"),
                            email=form.cleaned_data.get("email"),
                            password=make_password(
                                form.cleaned_data.get("password")),
                            type=form.cleaned_data.get("type"),
                            phone=form.cleaned_data.get("phone"),
                            address=form.cleaned_data.get("address"),
                            dob=form.cleaned_data.get("dob"),
                            profile=request.session.get("profile"),
                            created_user_id=user.id,
                            updated_user_id=user.id,
                            created_at=timezone.now(),
                            updated_at=timezone.now()
                        )
                        new_user.save()
                        request.session["create_update_confirm_page_flag"] = False
                        remove_temp(request.session.get("profile"))
                        return HttpResponseRedirect(reverse("user-list"))
                    else:
                        if "profile" in request.FILES:
                            profile = save_temp(request.FILES["profile"])
                            request.session["profile"] = profile
                            formData = {
                                "name": form.cleaned_data.get("name"),
                                "email": form.cleaned_data.get("email"),
                                "password": form.cleaned_data.get("password"),
                                "password_confirmation": form.cleaned_data.get("password_confirmation"),
                                "type": form.cleaned_data.get("type"),
                                "phone": form.cleaned_data.get("phone"),
                                "address": form.cleaned_data.get("address"),
                                "dob": form.cleaned_data.get("dob")
                            }
                            form = UserForm(initial=formData)
                            request.session["create_update_confirm_page_flag"] = True
                            form.fields["name"].widget.attrs["readonly"] = True
                            form.fields["email"].widget.attrs["readonly"] = True
                            form.fields["password"].widget.attrs["readonly"] = True
                            form.fields["password_confirmation"].widget.attrs["readonly"] = True
                            form.fields["type"].widget.attrs["readonly"] = True
                            form.fields["phone"].widget.attrs["readonly"] = True
                            form.fields["address"].widget.attrs["readonly"] = True
                            form.fields["dob"].widget.attrs["readonly"] = True
                            form.fields["profile"].widget.attrs["disabled"] = True
                        else:
                            request.session["save_confirm_page"] = False
                            form.add_error("profile", "profile can't be blank")
            else:
                request.session["create_update_confirm_page_flag"] = False
                return HttpResponseRedirect(reverse("user-create"))
    except Exception as e:
        print(str(e))
        form.add_error(None, str(e))
    context = {
        "title": "User Create",
        "form": form,
        "operation": "create",
        "create_update_confirm_page_flag": request.session["create_update_confirm_page_flag"]
    }
    return render(request, "posts/users_form.html", context)


@login_required
def user_update(request, pk):
    """
    View function for user update page of site.
    Param request user post form and file data.
    Return user update view.
    """
    req_user = get_object_or_404(User, pk=pk)
    profile = ""

    if req_user.profile and hasattr(req_user.profile, "url"):
        profile = req_user.profile.url
        profile = "/media/" + profile.split("/")[-1]
    else:
        profile = "/media/user-default.png"
    check_route("user", request.META.get("HTTP_REFERER"), request)
    formData = {
        "name": req_user.name,
        "email": req_user.email,
        "type": req_user.type,
        "phone": req_user.phone,
        "dob": req_user.dob,
        "address": req_user.address,
        "profile": profile
    }
    form = UserEditForm(initial=formData)
    if request.session.get("create_update_confirm_page_flag") is None:
        request.session["create_update_confirm_page_flag"] = False
    if request.method == "POST":
        if "_save" in request.POST:
            form = UserEditForm(request.POST, request.FILES)
            if form.is_valid():
                if request.session.get("create_update_confirm_page_flag") == True:
                    try:
                        oldFileDir = str(profile)
                        if oldFileDir != request.session.get("profile"):
                            file_dir = request.session.get("profile")
                            file_name = file_dir.split("/")[-1]
                            handle_uploaded_file(file_name)
                            remove_temp(file_name)
                            request.session["profile"] = file_name
                        user = get_object_or_404(User, pk=request.user.id)
                        user.name = form.cleaned_data.get("name")
                        user.email = form.cleaned_data.get("email")
                        user.type = form.cleaned_data.get("type")
                        user.phone = form.cleaned_data.get("phone")
                        user.dob = form.cleaned_data.get("dob")
                        user.address = form.cleaned_data.get("address")
                        user.profile = request.session.get("profile")
                        user.updated_user_id = user.id
                        user.updated_at = timezone.now()
                        user.save()
                        request.session["create_update_confirm_page_flag"] = False
                        return HttpResponseRedirect(reverse("user-list"))
                    except Exception as error:
                        request.session["create_update_confirm_page_flag"] = False
                        form.add_error(None, str(error))
                else:
                    if "profile" in request.FILES:
                        profile = save_temp(request.FILES["profile"])
                        request.session["profile"] = "/media/temp/" + profile
                    else:
                        request.session["profile"] = str(profile)
                    formData = {
                        "name": form.cleaned_data.get("name"),
                        "email": form.cleaned_data.get("email"),
                        "type": form.cleaned_data.get("type"),
                        "phone": form.cleaned_data.get("phone"),
                        "dob": form.cleaned_data.get("dob"),
                        "address": form.cleaned_data.get("address"),
                    }
                    form = UserEditForm(initial=formData)
                    request.session["create_update_confirm_page_flag"] = True
                    form.fields["name"].widget.attrs["readonly"] = True
                    form.fields["email"].widget.attrs["readonly"] = True
                    form.fields["type"].widget.attrs["readonly"] = True
                    form.fields["phone"].widget.attrs["readonly"] = True
                    form.fields["dob"].widget.attrs["readonly"] = True
                    form.fields["address"].widget.attrs["readonly"] = True
                    form.fields["profile"].widget.attrs["disabled"] = True
        else:
            request.session["create_update_confirm_page_flag"] = False
            return HttpResponseRedirect(reverse("user-update", kwargs={"pk": pk}))
    context = {
        "title": "Profile Edit",
        "id": req_user.id,
        "form": form,
        "old_profile":  req_user.profile,
        "profile": profile,
        "create_update_confirm_page_flag": request.session.get("create_update_confirm_page_flag")
    }
    return render(request, "posts/user_update.html", context)


@login_required
def user_profile(request):
    """
    View function for user profile page of site.
    Param request user id.
    Return user profile view.
    """
    current_user = get_object_or_404(User, pk=request.user.id)
    profile_url = ""
    if current_user.profile and hasattr(current_user.profile, "url"):
        profile_url = current_user.profile.url
        profile_url = "/media/" + profile_url.split("/")[-1]
    else:
        profile_url = "/media/user-default.png"
    context = {
        "id": current_user.id,
        "name": current_user.name,
        "type": current_user.type,
        "email": current_user.email,
        "phone": current_user.phone,
        "dob": current_user.dob,
        "address": current_user.address,
        "profile": profile_url,
        "title": "Post List"
    }
    return render(request, "posts/user_profile.html", context=context)


@login_required
def download_post_list_csv(request):
    """
    View function for download post list csv.
    Param request view reqest.
    Return download post list page view.
    """
    post_list = Post.objects.all()
    response = HttpResponse(content_type="text/csv")
    current_date_and_time = datetime.now()
    file_name = str(current_date_and_time) + "post_list.csv"
    response["Content-Disposition"] = "attachment; filename=" + file_name
    writer = csv.writer(response)
    writer.writerow(["id", "title", "description", "status", "created_user_id",
                    "updated_user_id", "deleted_user_id", "deleted_at", "created_at", "updated_at"])

    for post in post_list:
        writer.writerow([post.id, post.title, post.description, post.status, post.created_user_id,
                        post.updated_user_id, post.deleted_user_id, post.deleted_at, post.created_at, post.updated_at])
    return response


def check_csv_row(data):
    """
    check csv rows and add data to csv arrays.
    Param post list data.
    Return csv data array to download.
    """
    arr_csv = []
    for row in data:
        if len(row) != 3:
            return False
        arr_csv.append(row)
    return arr_csv


@login_required
def csv_import(request):
    """
    View csv import .
    Param request view reqest.
    Return import post list page view.
    """
    form = CSVForm()
    message = ""
    if request.method == "POST":
        try:
            form = CSVForm(request.POST, request.FILES)
            if "csv_file" in request.FILES:
                user = get_object_or_404(User, pk=request.user.id)
                req_file = request.FILES["csv_file"]
                csv_path = save_temp(req_file)
                with open("media/temp/{}".format(csv_path)) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    valid_csv = check_csv_row(csv_reader)
                    if valid_csv:
                        for i, row in enumerate(valid_csv):
                            if i != 0:
                                csv_post = Post(
                                    title=row[0],
                                    description=row[1],
                                    status=row[2],
                                    user=user,
                                    created_user_id=user.id,
                                    updated_user_id=user.id,
                                    created_at=timezone.now(),
                                    updated_at=timezone.now()
                                )
                                csv_post.save()
                        csv_file.close()
                        remove_temp(csv_path)
                        return HttpResponseRedirect(reverse("index"))
                    else:
                        message = "Post upload csv must have 3 columns"
            else:
                message = "Please choose a file"
        except Exception as e:
            message = str(e)
    context = {
        "title": "Upload CSV File",
        "form": form,
        "err_message": message
    }
    return render(request, "posts/csv-import.html", context=context)


def signup(request):
    """
    View signup page.
    Param django request view.
    Return signup page view.
    """
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = User(
                name=form.cleaned_data.get("name"),
                email=form.cleaned_data.get("email"),
                password=make_password(form.cleaned_data.get("password")),
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            new_user.save()
            authUser = authenticate(request, username=form.cleaned_data.get(
                "email"), password=form.cleaned_data.get("password"))
            if authUser:
                login(request, authUser)
                request.session["login_username"] = form.cleaned_data.get(
                    "name")
            messages.info(request, f"User signup successful.")
            return HttpResponseRedirect(reverse("index"))
    context = {
        "title": "Sign Up",
        "form": form
    }
    return render(request, "registration/sign_up.html", context)


@login_required
def post_delete(request):
    """
    View post delete page.
    Param post id.
    Return post list page.
    """
    post_id = request.GET["post_id"]
    delete_post = get_object_or_404(Post, pk=post_id)
    delete_post.deleted_user_id = request.user.id
    delete_post.deleted_at = timezone.now()
    delete_post.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
def user_delete(request):
    """
    View user delete page.
    Param user id.
    Return user list page.
    """
    user_id = request.GET["user_id"]
    delete_user = get_object_or_404(User, pk=user_id)
    delete_user.deleted_user_id = request.user.id
    delete_user.deleted_at = timezone.now()
    delete_user.save()
    return HttpResponseRedirect(reverse("user-list"))


@login_required
def password_change(request):
    """
    View user password reset page.
    Param password reset form data.
    Return password reset page.
    """
    reset_form = PasswordResetForm()
    if request.method == "POST":
        reset_form = PasswordResetForm(request.POST)
        if reset_form.is_valid():
            password = reset_form.cleaned_data.get("password")
            new_password = reset_form.cleaned_data.get("new_password")
            user = get_object_or_404(User, pk=request.user.id)
            if (check_password(password, user.password)):
                user.password = make_password(new_password)
                user.save()
                messages.info(request, f"Password is successfully updated.")
                return HttpResponseRedirect(reverse("user-list"))
            else:
                reset_form.add_error("password", "Current password is wrong!")
    return render(request, "registration/password_change.html", {"form": reset_form, "title": "Change Password"})
