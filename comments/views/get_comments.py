from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.pagination import PageNumberPagination

from comments.models import CommentMessage
from comments.serializers.comment import CommentSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CommentsListView(generics.ListCreateAPIView):
    queryset = CommentMessage.objects.all().order_by('-pk')
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset

        if self.request.GET.get('parent_id') and self.request.GET.get('parent_type'):
            parent_id = self.request.GET.get('parent_id')
            parent_type = self.request.GET.get('parent_type')
            queryset = queryset.filter(parent_id=parent_id, parent_type=parent_type)

        if self.request.GET.get('flat') == '0':
            id_list = list(queryset.values_list('id', flat=True))
            nested_comments = CommentMessage.objects.\
                filter(parent_id_list__overlap=id_list)
            queryset = queryset | nested_comments
            queryset = queryset.extra(select={'nested_depth': 'coalesce(array_length(parent_id_list,1), 0)'}). \
                        order_by('nested_depth', '-created_at')


        return queryset