from django.contrib import admin
from.models import CommentMessage
from reversion.admin import VersionAdmin

class BaseReversionAdmin(VersionAdmin):
 pass

admin.site.register(CommentMessage, BaseReversionAdmin)