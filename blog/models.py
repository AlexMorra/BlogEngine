from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from time import time

from taggit.managers import TaggableManager
from likes.models import LikeDislike


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    text = models.TextField(max_length=10000)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = GenericRelation(LikeDislike, default=0,
                            related_query_name='posts')
    tags = TaggableManager()

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = GenericRelation(LikeDislike, default=0,
                            related_query_name='comments')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.text