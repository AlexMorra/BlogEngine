from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from users.views import ProfileView


urlpatterns = [
    path('admin112/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    #path('', include('pages.urls')),
    path('', include('blog.urls')),
    path('api/', include('likes.urls')),

    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
]
urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
