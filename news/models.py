from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_of_posts = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] * 3
        rating_of_comments_by_author = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        rating_of_comments_by_users = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        
        self.rating = rating_of_posts + rating_of_comments_by_author + rating_of_comments_by_users
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Post(models.Model):
    news = 'NW'
    article = 'AR'

    POST_TYPES = [(news, 'Новость'), (article, 'Статья')]
    
    author = models.ForeignKey('Author', on_delete=models.PROTECT)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=article,)
    time_create = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=80, default='Заголовок')
    post_text = models.TextField(default='Текст статьи')
    rating = models.IntegerField(default=0)

    def preview(self):
        return f'{self.post_text[:124]}...' if len(self.post_text) > 124 else self.post_text
    
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment_text = models.TextField(default='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()