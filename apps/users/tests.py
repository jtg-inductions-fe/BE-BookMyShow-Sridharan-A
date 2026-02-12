from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TestUserAuth(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="user1@gmail.com",
            password="user@123",
            first_name="user1",
            last_name="A",
            phone_number="9876543210",
        )

    # Register

    def test_register_success(self):
        data = {
            "email": "new@gmail.com",
            "password": "user@123",
            "first_name": "Jane",
            "last_name": "Doe",
            "phone_number": "9876543210",
        }

        res = self.client.post("/api/auth/register/", data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["message"], "User registered successfully")

        user = User.objects.get(email="new@gmail.com")
        self.assertEqual(user.first_name, "Jane")
        self.assertTrue(user.check_password("user@123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_register_email_normalized(self):
        self.client.post(
            "/api/auth/register/",
            {
                "email": "UPPER@gmail.COM",
                "password": "user@123",
                "first_name": "Upper",
            },
        )

        self.assertTrue(User.objects.filter(email="upper@gmail.com").exists())

    def test_register_duplicate_email(self):
        res = self.client.post(
            "/api/auth/register/",
            {
                "email": self.user.email,
                "password": "user@123",
                "first_name": "duplicateuser",
            },
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Login

    def test_login_success(self):
        res = self.client.post(
            "/api/auth/login/",
            {
                "email": self.user.email,
                "password": "user@123",
            },
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_login_wrong_password(self):
        res = self.client.post(
            "/api/auth/login/",
            {
                "email": self.user.email,
                "password": "wrongpassword",
            },
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Helpers

    def authenticate(self):
        res = self.client.post(
            "/api/auth/login/",
            {
                "email": self.user.email,
                "password": "user@123",
            },
        )

        access = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    # User Profile

    def test_get_user_profile(self):
        self.authenticate()

        res = self.client.get("/api/auth/user/")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["email"], self.user.email)
        self.assertEqual(res.data["first_name"], self.user.first_name)

    def test_update_user_profile(self):
        self.authenticate()

        res = self.client.patch(
            "/api/auth/user/",
            {
                "first_name": "Updated",
                "phone_number": "9999999999",
            },
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.phone_number, "9999999999")

    def test_user_profile_requires_authentication(self):
        res = self.client.get("/api/auth/user/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
