from django import forms
from blog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class AnonymousCommentForm(forms.ModelForm):
    author_name = forms.CharField(required=True)
    author_email = forms.EmailField(required=True)

    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'text']
