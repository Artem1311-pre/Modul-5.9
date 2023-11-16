from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView

from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.core.paginator import Paginator


class PostList(PermissionRequiredMixin, ListView):
    permission_required = ('<post>.<add>_<news>',
                           '<post>.<create>_<news>',
                           '<post>.<delete>_<news>',
                           '<post>.<change>_<news>')
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):

        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        context['next_news'] = None
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'posts'
    pk_url_kwarg = 'id'

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):

        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'NW'
        news.save()
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'news_edit.html'

class NewsDelete(DeleteView):
    form_class = PostForm
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'AR'
        news.save()
        return super().form_valid(form)

class ArticlesUpdate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

class ArticlesDelete(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')





