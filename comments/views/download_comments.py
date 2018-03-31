import dicttoxml
from django.http import HttpResponse, StreamingHttpResponse

from comments.models import CommentMessage
from rest_framework_xml.renderers import XMLRenderer

formats_content_types = {
    'xml': 'application/xml'
}

def download_comments(request, format):
    queryset = CommentMessage.objects.all()
    return StreamingHttpResponse(xml_serialize(queryset))



def xml_serialize(queryset):
    yield '<comments>'
    output_fields = ['id', 'text', 'created_at', 'updated_at', 'parent_id', 'parent_type', 'user_id']
    renderer = XMLRenderer()
    for item in queryset.iterator():
        output_object = {k:getattr(item, k) for k in output_fields}
        yield dicttoxml.dicttoxml(output_object, root=False)
    yield '</comments>'


formats_serializers = {
    'xml': xml_serialize
}