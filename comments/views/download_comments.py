import dicttoxml
from django.http import StreamingHttpResponse, Http404

from comments.models import CommentMessage


def download_comments(request, format):
    queryset = CommentMessage.objects.all()
    if format in formats_serializers:
        return StreamingHttpResponse(formats_serializers[format](queryset))
    else:
        raise Http404


def xml_serialize(queryset):
    yield '<comments>'
    output_fields = ['id', 'text', 'created_at',
                     'updated_at', 'parent_id', 'parent_type',
                     'user']
    for item in queryset.iterator():
        yield '<message>'
        output_object = {k: getattr(item, k) for k in output_fields}
        yield dicttoxml.dicttoxml(output_object, root=False)
        yield '</message>'
    yield '</comments>'


formats_serializers = {
    'xml': xml_serialize
}
