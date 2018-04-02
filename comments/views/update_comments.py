from rest_framework import generics

from comments.models import CommentMessage
from comments.serializers.comment import CommentSerializer


class CommentSingleView(generics.RetrieveUpdateDestroyAPIView):
    model = CommentMessage
    serializer_class = CommentSerializer


    def get_queryset(self):
        return self.model.objects.filter(deleted=False)