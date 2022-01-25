import datetime
from django.utils import timezone
from django.test import RequestFactory, TestCase
from django.urls import reverse

from posts.models import Post, User


class LoginViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="1234")
        test_user.type = "1"
        test_user.save()

    def test_login_initial_view(self):
        response = self.client.get(reverse("user_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "registration/login.html"
        )

    def test_login_invalid_email(self):
        res_invalid_email = self.client.post(
            reverse("user_login"), {"email": "wrong@test.mm", "password": ""})
        messages = list(res_invalid_email.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email does not exist or deleted")

    def test_login_invalid_password(self):
        res_invalid_pass = self.client.post(
            reverse("user_login"), {"email": "test@user.com", "password": "wrong"})
        messages = list(res_invalid_pass.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Email and Password does not match.")

    def test_login(self):
        response = self.client.post("http://127.0.0.1:8000/accounts/login/?next=/posts/", {
                                    "email": "test@user.com", "password": "1234"})
        print('------------response------------')
        print(response)
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, "/posts/")


class PostListViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="1234")
        test_user.type = "1"
        test_user.save()
        # Create post
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

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/')

    def test_redirect_if_logged_in(self):
        self.client.login(email="test@user.com", password="1234")
        response = self.client.get(reverse("index"))
        self.assertEqual(len(response.context["page_obj"]), 1)
        self.assertEqual(response.context["page_obj"][0].title, "post of test")
        self.assertEqual(
            response.context["page_obj"][0].description, "This post is created by tester ...")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "index.html"
        )

    def test_form_post_search(self):
        self.client.login(email="test@user.com", password="1234")
        response = self.client.post(
            reverse("index"), {"_search": True, "keyword": "post of test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 1)

    def test_form_post_search_invalid(self):
        self.client.login(email="test@user.com", password="1234")
        response = self.client.post(
            reverse("index"), {"_search": True, "keyword": "xxxxx"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 0)

    def test_form_post_redirect_create(self):
        self.client.login(email="test@user.com", password="1234")
        response = self.client.post(
            reverse("index"), {"_create": True})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/post/create/")


# class UserListViewTest(TestCase):
#     def setUp(self):
#         test_user = User.objects.create_user(
#             email="test@user.com", password="1234")
#         test_user.type = "1"
#         test_user.save()
#         # user create
#         user = User.objects.create(
#             name="test001",
#             email="testuser@gmail.com",
#             password="tester1234",
#             profile="fake/path",
#             type="0",
#             phone="01234543",
#             address="yangon",
#             dob=timezone.now(),
#             created_user_id=test_user.id,
#             updated_user_id=test_user.id,
#             created_at=timezone.now(),
#             updated_at=timezone.now(),
#         )
#         user.save()

#     def test_user_list_without_login(self):
#         response = self.client.get(reverse("user-list"))
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(response.url == '/accounts/login?next=/users/')

#     def test_user_list_initial(self):
#         self.client.login(email="test@user.com", password="1234")
#         response = self.client.get(reverse("user-list"))
#         self.assertEqual(len(response.context["page_obj"]), 1)
#         self.assertEqual(
#             response.context["page_obj"][0].email, "testuser@gmail.com")
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(
#             response, "posts/user_list.html"
#         )

#     def test_user_list_search(self):
#         self.client.login(email="test@user.com", password="thePass129Z")
#         from_date = timezone.now() - datetime.timedelta(1)
#         to_date = timezone.now() + datetime.timedelta(1)
#         response = self.client.post(
#             reverse("user-list"),
#             {
#                 "name": "test001",
#                 "email": "test001@gmail.com"
#             }
#         )
#         self.assertEqual(len(response.context["page_obj"]), 1)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(
#             response, "posts/user_list.html"
#         )


# class PostCreateViewTest(TestCase):
#     def setUp(self):
#         test_user = User.objects.create_user(
#             email="test@user.com", password="thePass129Z")
#         test_user.type = "1"
#         test_user.save()
#         self.factory = RequestFactory()

#     def test_post_create_without_login(self):
#         response = self.client.get(reverse("post-create"))
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(response.url == '/accounts/login?next=/post/create/')

#     def test_post_create_initial(self):
#         self.client.login(email="test@user.com", password="thePass129Z")
#         response = self.client.get(reverse('post-create'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(
#             response, "posts/post-create.html"
#         )

#     def test_post_create_form_confirm(self):
#         self.client.login(email="test@user.com", password="thePass129Z")
#         response = self.client.post(
#             reverse('post-create'),
#             {"_save": True, "title": "test title",
#                 "description": "this is description"}
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(
#             response, "posts/post-create.html"
#         )

    # def test_post_create_form_create(self):
    #     self.client.login(email="test@user.com", password="thePass129Z")
    #     request = self.factory.get('post/create/')
    #     print(request.session.get("save_confirm_page"))
        
