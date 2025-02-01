from django.shortcuts import render
from rest_framework import viewsets
from .models import MarkdownContent
from .serializers import MarkdownContentSerializer

def markdownView(request):
    markdown_content = MarkdownContent.objects.first()
    context = {"markdown_content": markdown_content}
    return render(
        request,
        "Anubis/markdown.html",
        context=context
    )

class markdownRestView(viewsets.ModelViewSet):
    serializer_class = MarkdownContentSerializer
    queryset = MarkdownContent.objects.all()
