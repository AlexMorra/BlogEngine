from django.urls import path

from blog.views import (PostListView, PostDetailView, PostCreateView,
                        PostUpdateView, PostDeleteView)


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('tag/<str:tag>/', PostListView.as_view(), name='post_list'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<str:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('<str:slug>/update', PostUpdateView.as_view(), name='post_update'),
    path('<str:slug>/delete', PostDeleteView.as_view(), name='post_delete'),
]