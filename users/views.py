from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from users.models import CustomUser


class ProfileView(UpdateView, DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'blog/profile.html'
    fields = ['first_name', 'last_name', 'avatar']

    def get_success_url(self):
        url = self.object.get_absolute_url()
        return url


