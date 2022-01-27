import datetime
from unicodedata import name
from django.utils import timezone
from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from posts.models import Post, User


class LoginViewTest(TestCase):
    def setUp(self):
        """login view set up for test data"""
        test_user = User.objects.create_user(
            email="logintester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()
        self.user = User.objects.create(name="tester_login", email="tester_login@gmail.com")
        self.user.set_password("12345")
        self.user.save()

    def test_login_initial_view(self):
        """test login initial view"""
        response = self.client.get(reverse("user_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "registration/login.html"
        )

    def test_login_invalid_email(self):
        """test login invalid email"""
        res_invalid_email = self.client.post(
            reverse("user_login"), {"email": "wrong@test.mm", "password": ""})
        messages = list(res_invalid_email.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email does not exist or deleted")

    def test_login_invalid_password(self):
        """test login invalid password"""
        res_invalid_pass = self.client.post(
            reverse("user_login"), {"email": "logintester@gmail.com", "password": "wrong"})
        messages = list(res_invalid_pass.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Email and Password does not match.")

    def test_login(self):
        """test for login success"""
        response = self.client.post(reverse("user_login"), {
                                    "email": "logintester@gmail.com", "password": "12345"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/')

    def test_login_existed_username(self):
        """test for login user name existed"""
        response = self.client.post(reverse("user_login"), {
                                    "email": "tester_login@gmail.com", "password": "12345" })
        self.assertEqual(response.status_code, 302)

class PostListViewTest(TestCase):
    def setUp(self):
        """post list view set up data"""
        test_user = User.objects.create_user(
            email="postlisttester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()
        test_post = Post.objects.create(
            title="post of test",
            description="This post is created by tester ...",
            status="1",
            user=test_user,
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        test_post.save()
        session = self.client.session
        session["create_update_confirm_page_flag"] = True
        session.save()

    def test_redirect_if_not_logged_in(self):
        """test redirect login in login without authenticated."""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/posts/')

    def test_redirect_if_logged_in(self):
        """test redriect page after login"""
        self.client.login(email="postlisttester@gmail.com", password="12345")
        response = self.client.get(reverse("index"))
        self.assertEqual(len(response.context["page_obj"]), 1)
        self.assertEqual(response.context["page_obj"][0].title, "post of test")
        self.assertEqual(
            response.context["page_obj"][0].description, "This post is created by tester ...")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "posts/post_list.html"
        )

    def test_form_post_search(self):
        """test post search form"""
        self.client.login(email="postlisttester@gmail.com", password="12345")
        response = self.client.post(
            reverse("index"), {"keyword": "post of test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 1)

    def test_form_post_search_invalid(self):
        """test post search form invalid data"""
        self.client.login(email="postlisttester@gmail.com", password="12345")
        response = self.client.post(
            reverse("index"), {"keyword": "xxxxxxxxxxxxxxx"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 1)

class UserListViewTest(TestCase):
    def setUp(self):
        """set up data for user list view"""
        test_user = User.objects.create_user(
            email="userlisttester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()
        user = User.objects.create(
            name="tester1",
            email="userlisttester1@gmail.com",
            password="passwordTest11",
            profile="fake/path",
            type="0",
            phone="01234543",
            address="yangon",
            dob=timezone.now(),
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        user.save()

    def test_user_list_without_login(self):
        """test user list page without authenticated redirect login page"""
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/users/')

    def test_user_list_initial(self):
        """test user list page initial data"""
        self.client.login(email="userlisttester@gmail.com", password="12345")
        response = self.client.get(reverse("user-list"))
        self.assertEqual(len(response.context["page_obj"]), 1)
        self.assertEqual(
            response.context["page_obj"][0].email, "userlisttester1@gmail.com")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "posts/users_list.html"
        )

    def test_user_list_search(self):
        """test user list search"""
        self.client.login(email="userlisttester@gmail.com", password="12345")
        from_date = datetime.date.today()
        to_date = datetime.date.today()
        response = self.client.post(
            reverse("user-list"),
            {
                "name": "tester1",
                "email": "userlisttester1@gmail.com",
                "from_date": from_date,
                "to_date": to_date,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "posts/users_list.html"
        )


class PostCreateViewTest(TestCase):
    def setUp(self):
        """post create view for set up data"""
        test_user = User.objects.create_user(
            email="postcreatetester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()

    def test_post_create_without_login(self):
        """post create page without authentication redirect"""
        response = self.client.get(reverse("post-create"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/post/create/')

    def test_post_create_initial(self):
        """test post create template"""
        self.client.login(email="postcreatetester@gmail.com", password="12345")
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "posts/posts_form.html"
        )

    def test_post_create_form_confirm(self):
        """test post create confirm template"""
        self.client.login(email="postcreatetester@gmail.com", password="12345")
        response = self.client.post(
            reverse('post-create'),
            {"_save": True, "title": "test title",
                "description": "this is description"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "posts/posts_form.html"
        )

    def test_post_create_form_create(self):
        """test post create from confirm page"""
        self.client.login(email="postcreatetester@gmail.com", password="12345")
        session = self.client.session
        session["create_update_confirm_page_flag"] = True
        session.save()
        response = self.client.post(
            reverse('post-create'),
            {"_save": True, "title": "test title",
             "description": "this is description"}
        )
        self.assertEqual(response.status_code, 302)

    def test_post_create_form_cancel(self):
        """test post cancel from post create"""
        self.client.login(email="postcreatetester@gmail.com", password="12345")
        session = self.client.session
        session["create_update_confirm_page_flag"] = True
        session.save()
        self.client.get(reverse('post-create'))
        res_cancel = self.client.post(reverse("post-create"), {"_cancel": True, "title": "test title",
                                                               "description": "this is description"})
        self.assertEqual(res_cancel.status_code, 302)
        self.assertEqual(res_cancel.url, reverse("post-create"))


class UserCreateViewTest(TestCase):
    def setUp(self):
        """user create set up data"""
        test_user = User.objects.create_user(
            email="usercreatetester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()

    def test_user_create_without_login(self):
        """test user create page without login"""
        response = self.client.get(reverse("user-create"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/user/create/')

    def test_user_create_initial(self):
        """test user create initial template"""
        self.client.login(email="usercreatetester@gmail.com", password="12345")
        response = self.client.get(reverse('user-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "posts/users_form.html"
        )

    def test_user_create_from_confirm(self):
        """test user create from confirm page"""
        self.client.login(email="usercreatetester@gmail.com", password="12345")
        with open(str(settings.BASE_DIR)+"\\media\\test\\user_default.png", "rb") as profile:
            response = self.client.post(
                reverse('user-create'),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "usercreatetestermail1@gmail.com",
                    "password": "12345",
                    "password_confirmation": "12345",
                    "type": "0",
                    "phone": "09123456",
                    "profile": profile,
                    "address": "Yangon",
                }
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(
                response, "posts/users_form.html"
            )

    def test_user_create_form_withoutfile(self):
        """test user create without file"""
        self.client.login(email="usercreatetester@gmail.com", password="12345")
        response = self.client.post(
            reverse('user-create'),
            {
                "_save": True,
                "name": "test name",
                "email": "usercreatetestermail@gmail.com",
                "password": "12345",
                "password_confirmation": "12345",
                "type": "0",
                "phone": "09123456",
                "address": "Yangon"
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_user_create_exist_email(self):
        """test user create with file"""
        self.client.login(email="usercreatetester@gmail.com", password="12345")
        session = self.client.session
        session["create_update_confirm_page_flag"] = True
        session["profile"] = "user_default.png"
        session.save()
        with open(str(settings.BASE_DIR)+"\\media\\test\\user_default.png", "rb") as profile:
            response = self.client.post(
                reverse('user-create'),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "usercreatetester@gmail.com",
                    "password": "12345",
                    "password_confirmation": "12345",
                    "type": "0",
                    "phone": "09123456",
                    "profile": profile,
                    "address": "Yangon",
                }
            )

    def test_user_create_form_cancel(self):
        """test user create from cancel"""
        self.client.login(email="usercreatetester@gmail.com", password="12345")
        session = self.client.session
        session["create_update_confirm_page_flag"] = True
        session.save()
        self.client.get(reverse('user-create'))
        with open(str(settings.BASE_DIR)+"\\media\\test\\user_default.png", "rb") as profile:
            res_cancel = self.client.post(
                reverse('user-create'),
                {
                    "_cancel": True,
                    "name": "test name",
                    "email": "usercreatetestermail1@gmail.com",
                    "password": "12345",
                    "password_confirmation": "12345",
                    "type": "0",
                    "phone": "09123456",
                    "address": "Yangon",
                    "profile": profile
                }
            )
            self.assertEqual(res_cancel.status_code, 302)
            self.assertEqual(res_cancel.url, reverse("user-create"))

    def test_user_create_form_create(self):
        """test user create from create"""
        self.client.login(email="usercreatetester@gmail.com", password="12345")
        session = self.client.session
        session["create_update_confirm_page_flag"] = True
        session["profile"] = "user_default.png"
        session.save()
        with open(str(settings.BASE_DIR)+"\\media\\test\\user_default.png", "rb") as profile:
            response = self.client.post(
                reverse('user-create'),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "usercreatetestermail1@gmail.com",
                    "password": "12345",
                    "password_confirmation": "12345",
                    "type": "0",
                    "phone": "09123456",
                    "profile": profile,
                    "address": "Yangon",
                }
            )
            self.assertEqual(response.status_code, 302)


class PostUpdateViewTest(TestCase):
    def setUp(self):
        """test post update view set up data"""
        test_user = User.objects.create_user(
            email="postupdatetester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()

        self.test_post = Post.objects.create(
            title="test title",
            description="Hello world!!",
            status="1",
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_post_update_without_login(self):
        """test post update page without login redirect to login page"""
        response = self.client.get(
            reverse("post-update",  kwargs={'pk': self.test_post.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url == "/accounts/login?next=/post/{}/update/".format(str(self.test_post.id)))

    def test_post_update_initial(self):
        """test post update initial data"""
        self.client.login(email="postupdatetester@gmail.com", password="12345")
        response = self.client.get(
            reverse('post-update', kwargs={'pk': self.test_post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "posts/posts_form.html"
        )

    def test_post_update_form_confirm(self):
        """test post update confirm"""
        self.client.login(email="postupdatetester@gmail.com", password="12345")
        response = self.client.post(
            reverse('post-update',  kwargs={'pk': self.test_post.id}),
            {"_save": True, "title": "update test title",
                "description": "this is description update", "post_status": "0"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "posts/posts_form.html"
        )

    def test_post_update_form_confirm_without_status(self):
        """test post update without status"""
        self.client.login(email="postupdatetester@gmail.com", password="12345")
        response = self.client.post(
            reverse('post-update',  kwargs={'pk': self.test_post.id}),
            {"_save": True, "title": "update test title",
                "description": "this is description update"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "posts/posts_form.html"
        )

    def test_post_update_form_edit(self):
        """test post update after confirm"""
        self.client.login(email="postupdatetester@gmail.com", password="12345")
        session = self.client.session
        session["create_update_confirm_page_flag"] = True
        session['status'] = "0"
        session.save()
        response = self.client.post(
            reverse('post-update',  kwargs={'pk': self.test_post.id}),
            {"_save": True, "title": "update title",
             "description": "this is update description"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))

    def test_post_update_form_cancel(self):
        """test post cancel from confirm page"""
        self.client.login(email="postupdatetester@gmail.com", password="12345")
        session = self.client.session
        session["create_update_confirm_page_flag"] = True
        session.save()
        self.client.get(
            reverse('post-update', kwargs={'pk': self.test_post.id}),)
        res_cancel = self.client.post(reverse('post-update', kwargs={'pk': self.test_post.id}),
                                      {"_cancel": True, "title": "test title",
                                       "description": "this is description"})
        self.assertEqual(res_cancel.status_code, 302)
        self.assertEqual(res_cancel.url, reverse(
            'post-update', kwargs={'pk': self.test_post.id}))


class PostDetail(TestCase):
    def setUp(self):
        """post detail page set up data"""
        test_user = User.objects.create_user(
            email="postdetailtester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()

        self.test_post = Post.objects.create(
            title="detail test",
            description="Hello world!!",
            status="1",
            user=test_user,
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_post_detail_without_login(self):
        """test post detail without login"""
        response = self.client.get(
            reverse("post-detail"), {"post_id": self.test_post.id})
        self.assertEqual(response.status_code, 302)

    def test_post_detail(self):
        """test post detail"""
        self.client.login(email="postdetailtester@gmail.com", password="12345")
        response = self.client.get(
            reverse('post-detail'), {"post_id": self.test_post.id})
        self.assertEqual(response.status_code, 200)


class PostDeleteConfirmTest(TestCase):
    def setUp(self):
        """test post delete setup data"""
        test_user = User.objects.create_user(
            email="postdeletetester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()

        self.test_post = Post.objects.create(
            title="delete test",
            description="Hello world!!",
            status="1",
            user=test_user,
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_post_delete_without_login(self):
        """test post delete without login"""
        response = self.client.get(
            reverse("post-delete"), {"user_id": self.test_post.id})
        self.assertEqual(response.status_code, 302)

    def test_post_delete(self):
        """test post delete after login"""
        self.client.login(email="postdeletetester@gmail.com", password="12345")
        response = self.client.get(
            reverse("post-delete"), {"post_id": self.test_post.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))


class UserProfileTest(TestCase):
    def setUp(self):
        """test user profile setup data"""
        test_user = User.objects.create_user(
            email="postdeletetester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()

        test_user = User.objects.create_user(
            email="testerprofile@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()

    def test_user_profile_without_login(self):
        """test user profile without login"""
        response = self.client.get(
            reverse("user-profile"))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_initial(self):
        """test user profile initial data"""
        self.client.login(email="postdeletetester@gmail.com", password="12345")
        response = self.client.get(
            reverse("user-profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["email"], "postdeletetester@gmail.com")

    def test_user_profile_without_image(self):
        """test user profile without image"""
        self.client.login(email="testerprofile@gmail.com", password="12345")
        response = self.client.get(
            reverse("user-profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["email"], "testerprofile@gmail.com")


class UserDetail(TestCase):
    def setUp(self):
        """test user detail setup data"""
        test_user = User.objects.create_user(
            email="userdetailtester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()
        self.user = User.objects.create(
            name="tester1",
            email="tester1@gmail.com",
            password="12345",
            profile="fake/path",
            type="0",
            phone="01234543",
            address="yangon",
            dob=timezone.now(),
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.user.save()

    def test_user_detail_without_login(self):
        """test user detail without login"""
        response = self.client.get(
            reverse("user-detail"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, 302)

    def test_user_detail(self):
        """test user profile without image"""
        self.client.login(email="userdetailtester@gmail.com", password="12345")
        response = self.client.get(
            reverse("user-detail"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, 200)


class UserDeleteTest(TestCase):
    def setUp(self):
        """test user delete setup data"""
        test_user = User.objects.create_user(
            email="userdeletetester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()
        self.user = User.objects.create(
            name="deleteUser",
            email="deleteuser@gmail.com",
            password="passwordTest11",
            profile="fake/path",
            type="0",
            phone="01234543",
            address="yangon",
            dob=timezone.now(),
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.user.save()

    def test_user_delete_without_login(self):
        """test user delete without login"""
        response = self.client.get(
            reverse("user-delete"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, 302)

    def test_user_delete(self):
        """test user delete"""
        self.client.login(email="userdeletetester@gmail.com", password="12345")
        response = self.client.get(
            reverse("user-delete"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/users/")


class CsvDownloadTest(TestCase):
    def setUp(self):
        """test csv download setup data"""
        test_user = User.objects.create_user(
            email="csvdownloadtester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()

        self.test_post = Post.objects.create(
            title="detail test",
            description="Hello world!!",
            status="1",
            user=test_user,
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.test_post.save()

    def test_csv_download_without_login(self):
        """test csv download without login"""
        response = self.client.get(
            reverse("post-list-download"))
        self.assertEqual(response.status_code, 302)

    def test_csv_download(self):
        """test csv download"""
        self.client.login(email="csvdownloadtester@gmail.com", password="12345")
        response = self.client.get(
            reverse("post-list-download"))
        self.assertEqual(response.status_code, 200)


class UserPasswordResetTest(TestCase):
    def setUp(self):
        """test password reset setup data"""
        test_user = User.objects.create_user(
            email="passwordresettester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()

    def test_password_reset_without_login(self):
        """test password reset without login"""
        response = self.client.get(
            reverse("post-list-download"))
        self.assertTrue(
            response.url == "/accounts/login?next=/post/list/download/")
        self.assertEqual(response.status_code, 302)

    def test_password_reset_with_wrong_password(self):
        """test password reset with wrong password"""
        self.client.login(email="passwordresettester@gmail.com", password="12345")
        response = self.client.post(reverse(
            "password_change"), {"password": "wrong111", "new_password": "12345", "new_password_confirm": "12345"})
        self.assertContains(response, "Current password is wrong!", html=True)

    def test_password_reset(self):
        """test password reset"""
        self.client.login(email="passwordresettester@gmail.com", password="12345")
        response = self.client.post(reverse(
            "password_change"), {"password": "12345", "new_password": "12345", "new_password_confirm": "12345"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("user-list"))


class SignUpViewTest(TestCase):
    def test_sign_up_initial(self):
        """test sign up initial setup data"""
        response = self.client.get(reverse("create_account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "registration/sign_up.html"
        )

    def test_sign_up(self):
        """test user sign up page"""
        response = self.client.post(reverse("create_account"), {
            "name": "test signup",
            "email": "signupview@gmail.com",
            "password": "12345",
            "password_confirmation": "12345",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))


class CsvImportViewTest(TestCase):
    def setUp(self):
        """test csv import for posts setup data"""
        test_user = User.objects.create_user(
            email="csvimporttester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()

    def test_csv_import_without_login(self):
        """test csv import without login"""
        res = self.client.get(reverse("csv-import"))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, '/accounts/login?next=/csv/import/')

    def test_csv_import_initial(self):
        """test csv import initial data"""
        self.client.login(email="csvimporttester@gmail.com", password="12345")
        response = self.client.get(reverse("csv-import"))
        self.assertTrue(response.status_code == 200)

    def test_csv_import_without_file(self):
        """test csv import without file"""
        self.client.login(email="csvimporttester@gmail.com", password="12345")
        response = self.client.post(reverse("csv-import"), {"csv_file": ""})
        self.assertEqual(
            response.context["err_message"], "Please choose a file")

    def test_csv_import_with_invalid_file(self):
        """test csv import with invalid file"""
        self.client.login(email="csvimporttester@gmail.com", password="12345")
        with open(str(settings.BASE_DIR)+"\\media\\test\\user_default.png", "rb") as csv_file:
            response = self.client.post(
                reverse("csv-import"), {"csv_file": csv_file})
            self.assertEqual(
                response.context["err_message"], "Please choose csv format")

    def test_csv_import_with_multi_role_file(self):
        """test csv import with wrong csv format file"""
        self.client.login(email="csvimporttester@gmail.com", password="12345")
        with open(str(settings.BASE_DIR)+"\\media\\test\\wrong_upload.csv", "rb") as csv_file:
            response = self.client.post(
                reverse("csv-import"), {"csv_file": csv_file})
            self.assertEqual(
                response.context["err_message"], "Post upload csv must have 3 columns")

    def test_csv_import(self):
        """test csv import with correct file"""
        self.client.login(email="csvimporttester@gmail.com", password="12345")
        with open(str(settings.BASE_DIR)+"\\media\\test\\upload.csv", "rb") as csv_file:
            response = self.client.post(
                reverse("csv-import"), {"csv_file": csv_file})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("index"))


class UserEditViewTest(TestCase):
    def setUp(self):
        """test user edit setup data"""
        test_user = User.objects.create_user(
            email="useredittester@gmail.com", password="12345")
        test_user.type = "1"
        test_user.save()
        self.user = test_user

    def test_user_update_without_login(self):
        """test user update without login"""
        response = self.client.get(
            reverse("user-update", kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 302)

    def test_user_update_initial(self):
        """test user update initial data"""
        self.client.login(email="useredittester@gmail.com", password="12345")
        response = self.client.get(
            reverse('user-update', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "posts/user_update.html"
        )

    def test_user_update_form_confirm(self):
        """test user update from confirm page"""
        self.client.login(email="useredittester@gmail.com", password="12345")
        response = self.client.post(
            reverse('user-update', kwargs={'pk': self.user.id}),
            {
                "_save": True,
                "name": "test name",
                "email": "useredittester@gmail.com",
                "password": "12345",
                "password_confirmation": "12345",
                "type": "0",
                "phone": "09123456",
                "address": "Yangon"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "posts/user_update.html"
        )

    def test_user_update_form_confirm_withfile(self):
        """test user update form with file"""
        self.client.login(email="useredittester@gmail.com", password="12345")
        with open(str(settings.BASE_DIR)+"\\media\\test\\user_default.png", "rb") as profile:
            response = self.client.post(
                reverse('user-update', kwargs={'pk': self.user.id}),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "useredittester@gmail.com",
                    "password": "12345",
                    "password_confirmation": "12345",
                    "type": "0",
                    "phone": "09123456",
                    "profile": profile,
                    "address": "Yangon",
                }
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(
                response, "posts/user_update.html"
            )

    def test_user_edit_form_cancel(self):
        """test user edit form form cancel"""
        self.client.login(email="useredittester@gmail.com", password="12345")
        session = self.client.session
        session["create_update_confirm_page_flag"] = True
        session["updated_image"] = True
        session.save()
        self.client.get(reverse('user-update', kwargs={'pk': self.user.id}))
        with open(str(settings.BASE_DIR)+"\\media\\test\\user_default.png", "rb") as profile:
            res_cancel = self.client.post(
                reverse('user-update', kwargs={'pk': self.user.id}),
                {
                    "_cancel": True,
                    "name": "test name",
                    "email": "useredittestermail@gmail.com",
                    "password": "12345",
                    "password_confirmation": "12345",
                    "type": "0",
                    "phone": "09123456",
                    "profile": profile,
                    "address": "Yangon"
                }
            )
            self.assertEqual(res_cancel.status_code, 302)
            self.assertEqual(res_cancel.url, reverse(
                'user-update', kwargs={'pk': self.user.id}))

    def test_user_edit_form_nofile(self):
        """test user edit without file."""
        self.client.login(email="useredittester@gmail.com", password="12345")
        session = self.client.session
        session["create_update_confirm_page_flag"] = True
        session["updated_image"] = False
        session["profile"] = ""
        session.save()
        response = self.client.post(
            reverse('user-update', kwargs={'pk': self.user.id}),
            {
                "_save": True,
                "name": "test name",
                "email": "useredittestermail@gmail.com",
                "type": "0",
                "phone": "09123456",
                "address": "Yangon"
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_user_edit_form_withfile(self):
        """test user edit with image"""
        self.client.login(email="tester@gmail.com", password="12345")
        session = self.client.session
        session["create_update_confirm_page_flag"] = False
        session["updated_image"] = True
        session.save()
        with open(str(settings.BASE_DIR)+"\\media\\test\\user_default.png", "rb") as profile:
            self.client.post(
                reverse('user-update', kwargs={'pk': self.user.id}),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "userupdatetester@gmail.com",
                    "type": "0",
                    "phone": "09123456",
                    "profile": profile,
                    "address": "Yangon"
                }
            )
            session["create_update_confirm_page_flag"] = True
            session["profile"] = "user_default.png"
            session.save()
            res = self.client.post(
                reverse('user-update', kwargs={'pk': self.user.id}),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "userupdatetester@gmail.com",
                    "type": "0",
                    "phone": "09123456",
                    "address": "Yangon"
                }
            )
            self.assertEqual(res.status_code, 302)
