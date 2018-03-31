from django.test import TestCase

from comments.models import CommentMessage
from users.models import User

class UsersTestCase(TestCase):
    def setUp(self):
        user = User.objects.create()
        root_comment = CommentMessage.objects.create(text="Test text", user=user, parent_id=1, parent_type="article")
        child_comment = CommentMessage.objects.create(text="Test text", user=user, parent_id=1, parent_type="comment")

    def test_animals_can_speak(self):
        first = User.objects.get(pk=1)
        second = User.objects.get(pk=2)
        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)