from django.test import TestCase
from posts.forms import PostForm, SeachPostForm, SignUpForm, UserEditForm, UserForm, SearchUserForm, PasswordResetForm, CSVForm


class SeachPostFormTest(TestCase):
    """Search Post Form Test Code"""
    def test_post_search_form(self):
        """test post search form label"""
        form = SeachPostForm()
        self.assertEqual(form.fields["keyword"].label, "keyword:")


class SearchUserFormTest(TestCase):
    """Search User Form Test Code"""
    def test_user_serarch_form(self):
        """test user search form label"""
        form = SearchUserForm()
        self.assertEqual(form.fields["name"].label, "Name :")
        self.assertEqual(form.fields["email"].label, "Email :")
        self.assertEqual(form.fields["from_date"].label, "From :")
        self.assertEqual(form.fields["to_date"].label, "To :")


class PostFormTest(TestCase):
    """Post Form Test Code"""
    def test_post_form_label(self):
        """test post search form label"""
        form = PostForm()
        self.assertTrue(form.fields["title"].label == "Title *")
        self.assertTrue(form.fields["description"].label == "Description *")

    def test_post_form_invalid(self):
        """test post form invalid"""
        form = PostForm(data={"title": "", "description": ""})
        self.assertFalse(form.is_valid())

    def test_post_form_description(self):
        """test post form invalid description"""
        form = PostForm(data={"title": "test", "description": "This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description."})
        self.assertFalse(form.is_valid())

    def test_post_form_valid(self):
        """test post form valid"""
        form = PostForm(data={"title": "test", "description": "test"})
        self.assertTrue(form.is_valid())


class UserFormTest(TestCase):
    """User Form Test Code"""
    def test_user_form_label(self):
        """test user form label"""
        form = UserForm()
        self.assertTrue(form.fields["name"].label == "Name *")
        self.assertTrue(form.fields["email"].label == "E-Mail Address *")
        self.assertTrue(form.fields["password"].label == "Password *")
        self.assertTrue(
            form.fields["password_confirmation"].label == "Password confirmation *")
        self.assertTrue(form.fields["type"].label == "Type")
        self.assertTrue(form.fields["phone"].label == "Phone")
        self.assertTrue(form.fields["dob"].label == "Date of birth")
        self.assertTrue(form.fields["address"].label == "Address")
        self.assertTrue(form.fields["profile"].label == "Profile *")

    def test_user_form_invalid(self):
        """test user form invalid"""
        form = UserForm(data={
            "name": "",
            "email": "",
            "type": "0",
            "password": "",
            "password_confirmation": "",
            "address": "",
            "profile": ""
        })
        self.assertFalse(form.is_valid())

    def test_user_form_invalid_email(self):
        """test user form invalid email"""
        form = UserForm(data={
            "name": "test",
            "email": "false mail",
            "type": "0",
            "password": "test",
            "password_confirmation": "test",
            "address": "Yangon",
            "profile": "test/path"
        })
        self.assertFalse(form.is_valid())

    def test_user_form_valid_email(self):
        """test user form valid email"""
        form = UserForm(data={
            "name": "test",
            "email": "mail@test.com",
            "type": "0",
            "password": "test",
            "password_confirmation": "test",
            "address": "Yangon",
            "profile": "test/path"
        })
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_password(self):
        """test user form invalid password"""
        form = UserForm(data={
            "name": "test",
            "email": "mail@test.com",
            "type": "0",
            "password": "test",
            "password_confirmation": "test12",
            "address": "Yangon",
            "profile": "test/path"
        })
        self.assertFalse(form.is_valid())

    def test_user_form_valid_password(self):
        """test user form valid password"""
        form = UserForm(data={
            "name": "test",
            "email": "mail@test.com",
            "type": "0",
            "password": "test",
            "password_confirmation": "test",
            "address": "Yangon",
            "profile": "test/path"
        })
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_type(self):
        """test user form invalid type"""
        form = UserForm(data={
            "name": "test",
            "email": "mail@test.com",
            "type": "",
            "password": "test",
            "password_confirmation": "test",
            "address": "Yangon",
            "profile": "test/path"
        })
        self.assertFalse(form.is_valid())

class UserEditFormTest(TestCase):
    """User Edit Form Test Code"""
    def test_user_edit_form_label(self):
        """test user edit form label"""
        form = UserEditForm()
        self.assertTrue(form.fields["name"].label == "Name *")
        self.assertTrue(form.fields["email"].label == "E-Mail Address *")
        self.assertTrue(form.fields["type"].label == "Type")
        self.assertTrue(form.fields["phone"].label == "Phone")
        self.assertTrue(form.fields["dob"].label == "Date of birth")
        self.assertTrue(form.fields["address"].label == "Address")
        self.assertTrue(form.fields["profile"].label == "Profile")

    def test_user_edit_form_invalid(self):
        """test user edit form invalid"""
        form = UserEditForm(data={
            "name": "",
            "email": ""
        })
        self.assertFalse(form.is_valid())

    def test_user_edit_form_invalid_email(self):
        """test user edit form invalid email"""
        form = UserEditForm(data={
            "name": "test",
            "email": "false mail",
            "type": "1",
            "address": "Yangon",
            "profile": "test/path"
        })
        self.assertFalse(form.is_valid())

    def test_user_edit_form_valid(self):
        """test user edit form valid"""
        form = UserEditForm(data={
            "name": "test",
            "email": "mail@test.com",
            "type": "1",
            "address": "Yangon",
            "profile": "test/path"
        })
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_type(self):
        """test user form invalid type"""
        form = UserForm(data={
            "name": "test",
            "email": "mail@test.com",
            "type": "",
            "address": "Yangon",
            "profile": "test/path"
        })
        self.assertFalse(form.is_valid())


class PasswordResetFormTest(TestCase):
    """Password Reset Form Test Code"""
    def test_reset_form_label(self):
        """test Password Reset Form label"""
        form = PasswordResetForm()
        self.assertEqual(form.fields["password"].label, "Current Password *")
        self.assertEqual(form.fields["new_password"].label, "New Password *")
        self.assertEqual(
            form.fields["new_password_confirm"].label, "New Confirm Password *")

    def test_password_reset_form_invalid(self):
        """test password rest form invalid"""
        form = PasswordResetForm(data={
            "password": "",
            "new_password": "",
            "new_password_confirm": ""
        })
        self.assertFalse(form.is_valid())

    def test_password_reset_form_password_invalid(self):
        """test password reset form password invalid"""
        form = PasswordResetForm(data={
            "password": "qwer1234",
            "new_password": "qwer4321",
            "new_password_confirm": "asdf1234"
        })
        self.assertFalse(form.is_valid())

    def test_password_reset_form_password_valid(self):
        """test password reset form password valid"""
        form = PasswordResetForm(data={
            "password": "qwer1234",
            "new_password": "qwer4321",
            "new_password_confirm": "qwer4321"
        })
        self.assertTrue(form.is_valid())


class SignUpFormTest(TestCase):
    """Sign Up Form Test Code"""
    def test_sign_up_form_label(self):
        """test signup form label"""
        form = SignUpForm()
        self.assertEqual(form.fields["name"].label, "Name *")
        self.assertEqual(form.fields["email"].label, "E-Mail Address *")
        self.assertEqual(form.fields["password"].label, "Password *")
        self.assertEqual(
            form.fields["password_confirmation"].label, "Password confirmation *")

    def test_password_reset_form_password_invalid(self):
        """test password reset form password invalid"""
        form = SignUpForm(data={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "12345",
            "password_confirmation": "123456"
        })
        self.assertFalse(form.is_valid())

    def test_password_reset_form_password_valid(self):
        """test password reset form password valid"""
        form = SignUpForm(data={
            "name": "tester",
            "email": "tester1@gmail.com",
            "password": "12345",
            "password_confirmation": "12345"
        })
        self.assertTrue(form.is_valid())
    
    def test_password_reset_form_password_valid(self):
        """test password reset form password valid"""
        form = SignUpForm(data={
            "name": "",
        })
        self.assertFalse(form.is_valid())


class CSVFormTest(TestCase):
    """CSV Form Test Code"""
    def test_csv_form_label(self):
        """test csv form label"""
        form = CSVForm()
        self.assertEqual(form.fields["csv_file"].label, "CSV file *")

    def test_file_invalid(self):
        """test file invalid"""
        form = CSVForm(data={
            "csv_file": ""
        })
        self.assertFalse(form.is_valid())
    
    def test_file_valid(self):
        """test file valid"""
        form = CSVForm(data={
            "csv_file": "test/path"
        })
        self.assertFalse(form.is_valid())