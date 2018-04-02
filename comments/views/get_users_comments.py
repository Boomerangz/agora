from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import JsonResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.pagination import PageNumberPagination

from comments.models import CommentMessage
from comments.serializers.comment import CommentSerializer
from users.models import User


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 20000


class UsersCommentsListView(generics.ListAPIView):
    queryset = CommentMessage.objects.all().order_by('-pk')
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        try:
            user = User.objects.get(pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404

        queryset = self.queryset.filter(user=user).order_by('-created_at')

        return queryset