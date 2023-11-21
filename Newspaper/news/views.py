from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.shortcuts import render, reverse, redirect
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from datetime import datetime
from django.shortcuts import get_object_or_404

from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from .models import Appointment

from .models import Post
from .filters import PostFilter
from .forms import PostForm


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'appointment/make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # получаем наш html
        html_content = render_to_string(
            'appointment/appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email='comrad.heisenberg@yandex.ru',
            to=['akochkin@toyotatt.ru'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

        return redirect('appointment_created')

class PostList(ListView):
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


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'NW'
        news.save()
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
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

class CategoryListView(PostList):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news_edit.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-created_at')
        return queryset

    def get_context_data(self,**kwargs):
        context = super.get_context_data(**kwargs)
        context['is_nor_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Здравствуйте!'
    return render(request, 'subscribe.html', {'category': category, 'message':message})





