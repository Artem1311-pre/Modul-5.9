from django.urls import path
from .views import (
   PostList, PostDetail,
   NewsCreate, PostSearch, NewsUpdate, NewsDelete,
   ArticlesCreate, ArticlesUpdate, ArticlesDelete)

from .import views


urlpatterns = [
   path('', PostList.as_view()),
   path('<int:id>', PostDetail.as_view(), name='news'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:id>/edit/', ArticlesUpdate.as_view(), name='articles_edit'),
   path('articles/<int:id>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   path('search/', PostSearch.as_view(), name='post_search'),
]

