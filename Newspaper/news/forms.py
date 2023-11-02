from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):

   class Meta:
       model = Post
       fields = {
       'author': ['icontains'],
       'title': ['icontains'],
       'text': ['icontains'],
       }
       # labels = {
       #     'author': _('Автоар'),
       #     'title' : _('Заголовок'),
       #     'article_news': _('Категория'),
       #     'text': _('Содержание'),
       # }
       def clean(self):
           cleaned_data = super().clean()
           author = cleaned_data.get("name")
           content = cleaned_data.get("content")

           if author == content:
               raise ValidationError(
                   "Содержание не должно быть идентичным названию."
               )

           return cleaned_data
