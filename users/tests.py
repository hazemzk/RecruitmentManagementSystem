from django.test import TestCase
from .models import User


class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            email="test@test.com",
            password="123456",
            full_name="Test User",
            role="job_seeker"
        )

        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.check_password("123456"))
        self.assertEqual(user.role, "job_seeker")