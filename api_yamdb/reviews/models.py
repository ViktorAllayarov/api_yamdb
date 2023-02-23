from django.db import models

from users.models import User


def get_rating(x):
    reviews = x.reviews.all()
    score = 0
    if reviews:
        for review in reviews:
            score += review.score
        return (score//len(reviews))
    return 0


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    def __init__(self):
        self.rating = get_rating(self)

    name = models.TextField()
    year = models.IntegerField()
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
    '''Модел Отзыва'''
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
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Comment(models.Model):
    '''Модель Комментария'''
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