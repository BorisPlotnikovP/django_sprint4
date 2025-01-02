from django.contrib.auth import get_user_model
from django.forms import DateTimeInput, ModelForm, Textarea

from .models import Comment, Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': DateTimeInput(attrs={'type': 'datetime-local'})
        }


class ProfileUpdateForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'rows': '4'})
        }
