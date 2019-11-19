from django import forms

from blog.models import Post, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text', 'post')

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),
        }
