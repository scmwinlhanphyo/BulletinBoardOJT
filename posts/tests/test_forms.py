from django.test import TestCase
from posts.forms import PostForm, SeachPostForm, SignUpForm, UserEditForm, UserForm, SearchUserForm, PasswordResetForm, CSVForm


class SeachPostFormTest(TestCase):
    def test_post_search_form(self):
        form = SeachPostForm()
        self.assertEqual(form.fields["keyword"].label, "keyword:")


class SearchUserFormTest(TestCase):
    def test_user_serarch_form(self):
        form = SearchUserForm()
        self.assertEqual(form.fields["name"].label, "Name :")
        self.assertEqual(form.fields["email"].label, "Email :")
        self.assertEqual(form.fields["from_date"].label, "From :")
        self.assertEqual(form.fields["to_date"].label, "To :")


class PostFormTest(TestCase):
    def test_post_form_label(self):
        form = PostForm()
        self.assertTrue(form.fields["title"].label == "Title *")
        self.assertTrue(form.fields["description"].label == "Description *")

    def test_post_form_invalid(self):
        form = PostForm(data={"title": "", "description": ""})
        self.assertFalse(form.is_valid())

    def test_post_form_description(self):
        form = PostForm(data={"title": "test", "description": "This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description. This is test description."})
        self.assertFalse(form.is_valid())

    def test_post_form_valid(self):
        form = PostForm(data={"title": "test", "description": "test"})
        self.assertTrue(form.is_valid())


class UserFormTest(TestCase):
    def test_user_form_label(self):
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
    def test_user_edit_form_label(self):
        form = UserEditForm()
        self.assertTrue(form.fields["name"].label == "Name *")
        self.assertTrue(form.fields["email"].label == "E-Mail Address *")
        self.assertTrue(form.fields["type"].label == "Type")
        self.assertTrue(form.fields["phone"].label == "Phone")
        self.assertTrue(form.fields["dob"].label == "Date of birth")
        self.assertTrue(form.fields["address"].label == "Address")
        self.assertTrue(form.fields["profile"].label == "Profile")

    def test_user_edit_form_invalid(self):
        form = UserEditForm(data={
            "name": "",
            "email": ""
        })
        self.assertFalse(form.is_valid())

    def test_user_edit_form_invalid_email(self):
        form = UserEditForm(data={
            "name": "test",
            "email": "false mail",
            "type": "1",
            "address": "Yangon",
            "profile": "test/path"
        })
        self.assertFalse(form.is_valid())

    def test_user_edit_form_valid(self):
        form = UserEditForm(data={
            "name": "test",
            "email": "mail@test.com",
            "type": "1",
            "address": "Yangon",
            "profile": "test/path"
        })
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_type(self):
        form = UserForm(data={
            "name": "test",
            "email": "mail@test.com",
            "type": "",
            "address": "Yangon",
            "profile": "test/path"
        })
        self.assertFalse(form.is_valid())


class PasswordResetFormTest(TestCase):
    def test_reset_form_label(self):
        form = PasswordResetForm()
        self.assertEqual(form.fields["password"].label, "Current Password *")
        self.assertEqual(form.fields["new_password"].label, "New Password *")
        self.assertEqual(
            form.fields["new_password_confirm"].label, "New Confirm Password *")

    def test_password_reset_form_invalid(self):
        form = PasswordResetForm(data={
            "password": "",
            "new_password": "",
            "new_password_confirm": ""
        })
        self.assertFalse(form.is_valid())

    def test_password_reset_form_password_invalid(self):
        form = PasswordResetForm(data={
            "password": "qwer1234",
            "new_password": "qwer4321",
            "new_password_confirm": "asdf1234"
        })
        self.assertFalse(form.is_valid())

    def test_password_reset_form_password_valid(self):
        form = PasswordResetForm(data={
            "password": "qwer1234",
            "new_password": "qwer4321",
            "new_password_confirm": "qwer4321"
        })
        self.assertTrue(form.is_valid())


class SignUpFormTest(TestCase):
    def test_sign_up_form_label(self):
        form = SignUpForm()
        self.assertEqual(form.fields["name"].label, "Name *")
        self.assertEqual(form.fields["email"].label, "E-Mail Address *")
        self.assertEqual(form.fields["password"].label, "Password *")
        self.assertEqual(
            form.fields["password_confirmation"].label, "Password confirmation *")

    def test_password_reset_form_password_invalid(self):
        form = SignUpForm(data={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "12345",
            "password_confirmation": "123456"
        })
        self.assertFalse(form.is_valid())

    def test_password_reset_form_password_valid(self):
        form = SignUpForm(data={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "12345",
            "password_confirmation": "12345"
        })
        self.assertTrue(form.is_valid())
    
    def test_password_reset_form_password_valid(self):
        form = SignUpForm(data={
            "name": "",
        })
        self.assertFalse(form.is_valid())


class CSVFormTest(TestCase):
    def test_csv_form_label(self):
        form = CSVForm()
        self.assertEqual(form.fields["csv_file"].label, "CSV file *")

    def test_file_invalid(self):
        form = CSVForm(data={
            "csv_file": ""
        })
        self.assertFalse(form.is_valid())
    
    def test_file_valid(self):
        form = CSVForm(data={
            "csv_file": "test/path"
        })
        self.assertFalse(form.is_valid())