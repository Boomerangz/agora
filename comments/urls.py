from django.conf.urls import url
from django.urls import path, re_path

from comments.views import CommentsListView
from comments.views.download_comments import download_comments
from comments.views.get_message_history import CommentsHistoryListView
from comments.views.get_users_comments import UsersCommentsListView
from comments.views.update_comments import CommentSingleView

print(download_comments)
urlpatterns = [
    url(r'^$', CommentsListView.as_view()),
    path('<int:pk>/', CommentSingleView.as_view()),
    path('<int:pk>/history/', CommentsHistoryListView.as_view()),
    path('users/<int:pk>/', UsersCommentsListView.as_view(), name='list_view'),
    path('download/comments.<format>', download_comments),
]
