from django.conf.urls import url

from comments.views import CommentsListView

urlpatterns = [
    url(r'^$', CommentsListView.as_view()),
]