from django.contrib import admin
from .models import CommentMessage
from reversion.admin import VersionAdmin

admin.site.register(CommentMessage, VersionAdmin)
