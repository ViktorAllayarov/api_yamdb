from django.contrib.auth.models import AbstractUser
from django.db import models

from users.models import User


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    top = models.IntegerField(null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        null=True,
    )


class Review(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name='reviews'
                               )
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False,
                              related_name='reviews'
                              )
    text = models.TextField()
    score = models.IntegerField(related_name='reviews')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name='comments'
                               )
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name='comments'
                               )
    text = models.TextField(blank=False,
                            null=False,)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('author', 'review',)
