import json
from random import random

from django.test import TestCase

from comments.models import CommentMessage
from users.models import User


def get_random_id():
    return int(random() * 200000)


class GetCommentsTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(GetCommentsTestCase, self).__init__(*args, **kwargs)
        self.user_id = None

    def setUp(self):
        user = User.objects.create()
        self.user_id = user.id

    def testAddComment(self):
        test_comment_data = {
            'text': 'Test comment 1',
            'parent_id': 1,
            'parent_type': 'article',
            'user': self.user_id
        }
        response = self.client.post('/comments/', test_comment_data)
        self.assertEqual(response.status_code, 201)

        response = json.loads(response.content)
        for key, value in test_comment_data.items():
            self.assertEqual(value, response[key])

        comment_id = response['id']
        comment_from_db = CommentMessage.objects.get(pk=comment_id)
        for key, value in test_comment_data.items():
            if key == "user":
                #cause of serialization
                key = "user_id"
            self.assertEqual(value, getattr(comment_from_db, key))


    def testAddCommentWithNonExistingUser(self):
        while True:
            random_user_id = get_random_id()
            if User.objects.filter(pk=random_user_id).count() == 0:
                break

        test_comment_data = {
            'text': 'Test comment 1',
            'parent_id': 1,
            'parent_type': 'article',
            'user': random_user_id
        }
        response = self.client.post('/comments/', test_comment_data)
        self.assertEqual(response.status_code, 400)

    def testAddCommentWithoutData(self):
        test_comment_data = {
            'parent_id': 1,
            'parent_type': 'article',
        }
        response = self.client.post('/comments/', test_comment_data)
        self.assertEqual(response.status_code, 400)





