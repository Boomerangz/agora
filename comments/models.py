import reversion
from django.contrib.postgres import fields as pg_fields
from django.db import models
from rest_framework.exceptions import PermissionDenied

from users.models import User

PARENT_TYPE_COMMENT = "comment"

@reversion.register()
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


    def delete(self, using=None, keep_parents=False):
        if CommentMessage.objects.filter(parent_id=self.id, parent_type=PARENT_TYPE_COMMENT).count() > 0:
            raise PermissionDenied
        else:
            self.deleted = True
            self.save()
