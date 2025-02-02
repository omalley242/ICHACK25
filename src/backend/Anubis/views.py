from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import MarkdownContent
from .serializers import MarkdownContentSerializer
from django.http import HttpResponse

def markdownView(request):
    markdown_content = MarkdownContent.objects.first()
    context = {"markdown_content": markdown_content}
    return render(
        request,
        "Anubis/markdown.html",
        context=context
    )

# class markdownRestView(viewsets.ModelViewSet):
#     serializer_class = MarkdownContentSerializer
#     queryset = MarkdownContent.objects.all()

class markdownRestView(viewsets.ReadOnlyModelViewSet):
    queryset = MarkdownContent.objects.all()
    serializer_class = MarkdownContentSerializer
    lookup_field = 'file_name'

    @action(detail=False)
    def file_names(self, request, pk=None):
        sorted_data = sorted([file.file_name for file in self.queryset])
        response = Response(sorted_data)
        return response
