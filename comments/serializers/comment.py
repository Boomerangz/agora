from rest_framework import serializers

from comments.models import CommentMessage


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentMessage
        fields = ('id', 'text', 'created_at', 'updated_at', 'parent_id', 'parent_type', 'user')