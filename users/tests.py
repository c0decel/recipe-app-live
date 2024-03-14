from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from users.models import User

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', name='Test User')


    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.name, 'Test User')
        self.assertTrue(self.user.check_password('password123'))
