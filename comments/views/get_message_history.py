from django.contrib.contenttypes.models import ContentType
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from comments.serializers.version import VerionsSerializer
from reversion.models import Version


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 20000


class CommentsHistoryListView(generics.ListAPIView):
    queryset = Version.objects.all().order_by('-pk')
    serializer_class = VerionsSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset.filter(object_id=self.kwargs['pk'], content_type=ContentType.objects.get(model='commentmessage').id).\
            order_by('-pk')

        return queryset