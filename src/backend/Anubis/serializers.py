from rest_framework import serializers
from .models import MarkdownContent

class MarkdownContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkdownContent
        fields = ('file_name', 'content')