import json
from urllib.parse import urlencode

from django.test import TestCase

from comments.models import CommentMessage
from users.models import User

class GetCommentsTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(GetCommentsTestCase, self).__init__(*args, **kwargs)
        self.comment_depth = 1000
        self.root_comment_count = 1000
        self.comment_id_list = set()

    def setUp(self):
        user = User.objects.create()

        for i in range(self.root_comment_count):
            root_comment = CommentMessage.objects.create(text="Test text %d" % (i+1), user=user, parent_id=1, parent_type="article")
            self.comment_id_list.add(root_comment.id)
        for i in range(self.comment_depth):
            child_comment = CommentMessage.objects.create(text="Child comment %d" % (i+1), user=user, parent_id=root_comment.id, parent_type="comment")
            self.comment_id_list.add(child_comment.id)
            root_comment = child_comment

    def test_receiving_all_comments(self):
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response['count'], self.comment_depth+self.root_comment_count)

    def test_receiving_root_comment(self):
        params = {
            'flat': 1, #Means we want to receive only comments for this entity without children
            'parent_type': 'article',
            'parent_id': 1
        }
        response = self.client.get('/comments/?%s' % urlencode(params))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response['count'], self.root_comment_count)



    def test_receiving_root_comment_with_children(self):
        params = {
            'flat': 0, #Means we want to receive all comments hierarchy starting from comments for this entity
            'parent_type': 'article',
            'parent_id': 1
        }
        response = self.client.get('/comments/?%s' % urlencode(params))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response['count'], self.comment_depth+self.root_comment_count)

        # check if can make an hierarchy from results
        comment_id_list = []
        for comment in response['results']:
            self.assertIn(comment['parent_type' ], ['article', 'comment'])
            comment_id_list.append(comment['id'])
            if comment['parent_type'] == 'article':
                self.assertEqual(comment['parent_id'], 1)
            elif comment['parent_type'] == 'comment':
                self.assertIn(comment['parent_id'], comment_id_list)


    def test_pagination(self):
        params = {
            'flat': 0,  # Means we want to receive all comments hierarchy starting from comments for this entity
            'parent_type': 'article',
            'parent_id': 1
        }
        response = self.client.get('/comments/?%s' % urlencode(params))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        while True:
            self.assertEqual(response['count'], self.comment_depth + self.root_comment_count)
            for comment in response['results']:
                self.assertIn(comment['id'], self.comment_id_list)
                self.comment_id_list.remove(comment['id'])

            if response['next']:
                response = self.client.get(response['next'])
                self.assertEqual(response.status_code, 200)
                response = json.loads(response.content)
            else:
                break

        self.assertEqual(len(self.comment_id_list), 0)
