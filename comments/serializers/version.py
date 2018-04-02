import json
from json import JSONEncoder

from rest_framework import serializers
from reversion.models import Version, Revision


class CustomJSONSerializer(serializers.ReadOnlyField):
    def to_representation(self, data):
        return json.loads(data)[0]['fields']


class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ('date_created', 'user')


class VerionsSerializer(serializers.ModelSerializer):
    revision = RevisionSerializer(read_only=True)
    serialized_data = CustomJSONSerializer()

    class Meta:
        model = Version
        fields = ('revision', 'serialized_data')
