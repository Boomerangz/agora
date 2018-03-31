from django.contrib.postgres import fields as pg_fields
from django.db import models

from users.models import User

PARENT_TYPE_COMMENT = "comment"


class CommentMessage(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #field of relation with parents
    parent_id = models.IntegerField(blank=False, null=False)
    parent_type = models.CharField(max_length=255, blank=False, null=False)

    parent_id_list = pg_fields.ArrayField(models.IntegerField(), blank=True)



    def save(self, *args, **kwargs):
        if self.parent_id_list is None:
            if self.parent_type == PARENT_TYPE_COMMENT:
                self.parent_id_list = CommentMessage.objects.get(pk=self.parent_id).parent_id_list + [self.parent_id]
            else:
                self.parent_id_list = []
        super(CommentMessage, self).save(*args, **kwargs)
