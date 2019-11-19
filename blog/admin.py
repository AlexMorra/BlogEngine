from django.contrib import admin

from blog.models import Post, Comment


class CommentInline(admin.TabularInline):  # admin.StackedInline
    model = Comment
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'status')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'status', 'created_at')  # 'votes'
    inlines = [
        CommentInline,
    ]
