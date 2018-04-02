from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from comments.models import CommentMessage
from comments.serializers.comment import CommentSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 20000


class UsersCommentsListView(generics.ListAPIView):
    queryset = CommentMessage.objects.all().order_by('-pk')
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.kwargs['pk']).order_by('-created_at')

        return queryset