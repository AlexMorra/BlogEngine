from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum
from django.contrib.auth import get_user_model


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # take queryset more then 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # take queryset less then 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # take sum rating
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def posts(self):
        return self.get_queryset().filter(content_type__model='post').order_by(
            '-articles__pub_date')

    def comments(self):
        return self.get_queryset().filter(content_type__model='comment').order_by(
            '-comments__pub_date')


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'like'),
        (LIKE, 'dislike')
    )

    vote = models.SmallIntegerField(verbose_name="vote", choices=VOTES)
    user = models.ForeignKey(get_user_model(), verbose_name="user", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    def __str__(self):
        return str(self.vote)