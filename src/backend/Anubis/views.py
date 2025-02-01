from django.shortcuts import render
from .models import MarkdownContent

def markdown_view(request):
    markdown_content = MarkdownContent.objects.first()
    context = {"markdown_content": markdown_content}
    return render(
        request,
        "Anubis/markdown.html",
        context=context
    )
