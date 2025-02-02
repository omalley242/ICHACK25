from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
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

# class markdownRestView(viewsets.ModelViewSet):
#     serializer_class = MarkdownContentSerializer
#     queryset = MarkdownContent.objects.all()

class markdownRestView(viewsets.ReadOnlyModelViewSet):
    queryset = MarkdownContent.objects.all()
    serializer_class = MarkdownContentSerializer
    lookup_field = 'file_name'

    @action(detail=False)
    def file_names(self, request, pk=None):
        """
        Returns a list of all the group names that the given
        user belongs to.
        """
        return Response(sorted([file.file_name for file in self.queryset]))
