from django.test import TestCase
from users.models import User

class UsersTestCase(TestCase):
    def setUp(self):
        User.objects.create()
        User.objects.create()

    def test_animals_can_speak(self):
        first = User.objects.get(pk=1)
        second = User.objects.get(pk=2)
        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)