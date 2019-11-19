from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from blog.models import Post
from blog.forms import CommentForm


class PostListView(ListView):
    """ List of posts or search by request """
    model = Post
    paginate_by = 3
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self, slug=None):
        queryset = self.request.GET.get('q')
        tag = self.kwargs.get('tag')
        if tag:
            queryset = Post.objects.all().filter(status=True).filter(tags__name=tag)
            print(queryset)
        elif queryset:
            queryset = Post.objects.filter(
                Q(title__icontains=queryset) | Q(text__icontains=queryset)
            ).filter(status=True)
        else:
            queryset = Post.objects.all().filter(status=True)
        return queryset


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse("post_detail", kwargs={"slug": self.object.slug})

    def get_initial(self):
        """ auto fill author field """
        return {"post": self.object, 'author': self.request.user}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['title', 'text', 'image', 'tags']

    def form_valid(self, form):
        """ auto fill author field """
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    fields = ['title', 'text', 'image', 'tags']


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')

    def delete(self, request, *args, **kwargs):
        """ Change status instead of deleting """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status = False
        self.object.save()
        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
