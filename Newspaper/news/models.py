from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from datetime import datetime

class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):

        articles_rating = \
            Post.objects.filter(author_id=self.id).aggregate(Sum('rating_news')).get('rating_news__sum') * 3
        # print(articles_rating)
        comments_rating = \
            Comment.objects.filter(author_id=self.id).aggregate(Sum('comment_rating')).get('comment_rating__sum')
        # print(comments_rating)
        comments_articles_rating = \
            Comment.objects.filter(post__author=self).aggregate(Sum('comment_rating')).get('comment_rating__sum')
        # print(comments_articles_rating)

        self.rating = articles_rating + comments_rating + comments_articles_rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    sport = 'SP'
    policy = 'PO'
    education = 'ED'
    culture = 'CU'
    technology = "TECH"

    POSITION = [
            (policy, 'Политика'),
            (culture, 'Культура'),
            (education, 'Образование'),
            (sport, 'Спорт'),
            (technology, 'Технологии')
    ]

    category = models.CharField(max_length=10, choices=POSITION, default=sport, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.category


class Post(models.Model):
    Article = "AT"
    News = "NW"

    POST_TYPES = [
        (Article, 'Статья'),
        (News, 'Новость'),
]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article_news = models.CharField(max_length=10, choices=POST_TYPES, default=News)
    date_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255,)
    text = models.TextField()
    rating_news = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_news += 1
        self.save()

    def dislike(self):
        self.rating_news -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def __str__(self):
        return (f'{self.title.title()}:{self.text.title()}:{self.date_in}:{self.author}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=False)
    comment_time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'

