from rest_framework import serializers
from .models import ReleaseApp
class ReleaseAppModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseApp
        fields = ["id", "name", "tag", "description","user"]