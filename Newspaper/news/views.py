from django.views.generic import ListView, DetailView
from .models import Author, Post

class Author(ListView):
    name = Author
    ordering = 'News'
    template_name = 'news.html'
    context_object_name = 'news'


class Post(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
