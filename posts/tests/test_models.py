import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from ..models import Post, User, UserManager


class PostModelTests(TestCase):
    """for Post db model for test code."""
    @classmethod
    def setUpTestData(cls):
        """set up post model test data."""
        Post.objects.create(title="test title", description='test description')

    def test_get_absolute_url(self):
        """post model get_absolute_url method"""
        post = Post.objects.get(id=1)
        self.assertEqual(post.get_absolute_url(), "/posts/")

    def test_post_str_(self):
        """post model str method"""
        post = Post.objects.get(id=1)
        self.assertEqual(post.__str__(), "test title")

class UserModelTests(TestCase):
    """for User db model for test code."""
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        User.objects.create(
            name="tester",
            email="usermodeltester@gmail.com",
            password="12345",
            profile="test/profile",
            type="0",
            phone="12345",
            address="Yangon",
            dob=timezone.now()
        )

    def test_user_str_(self):
        """user model str method"""
        user = User.objects.get(id=1)
        self.assertEqual(user.__str__(), "usermodeltester@gmail.com")


    def test_user_has_perm(self):
        """test user has perm"""
        user = User.objects.get(id=1)
        self.assertEqual(user.has_perm(None), True)

    def test_has_module_perms(self):
        """test has module perms"""
        user = User.objects.get(id=1)
        self.assertEqual(user.has_module_perms(None), True)

    def test_staff_user_register(self):
        """test user with staff"""
        user = User.objects.create_staffuser("teststaffuser@gmail.com", "12345")
        self.assertEqual(user.staff, True)
        self.assertEqual(user.active, True)
        self.assertEqual(user.email, "teststaffuser@gmail.com")

    def test_create_super_user(self):
        """create super user"""
        user = User.objects.create_superuser("testsuperuser@example.com", "12345")
        self.assertEqual(user.staff, True)
        self.assertEqual(user.active, True)
        self.assertEqual(user.admin, True)
        self.assertEqual(user.email, "testsuperuser@example.com")

    def test_user_create_without_mail(self):
        """test user create without email data"""
        try:
            User.objects.create_user(None, "1234")
        except ValueError:
            pass
        else:
            self.assertRaises(
                ValueError,
                "Users must have an email address"
            )