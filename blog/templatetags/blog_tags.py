from django import template
from django.db.models import Count

from blog.models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.all().filter(status=True).count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.all().filter(status=True).order_by('-created_at')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/post/most_commented_posts.html')
def get_most_commented_posts(count=3):
    most_commented_posts = Post.objects.all().filter(status=True).annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'most_commented_posts': most_commented_posts}


@register.filter(name='range')
def filter_range(start, end):
  return range(start, end+1)


@register.filter
def user_in(objects, user):
    if user.is_authenticated:
        return objects.filter(user=user).exists()
    return False


