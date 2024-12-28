from django.forms import ModelForm, DateTimeInput

from django.contrib.auth import get_user_model

from .models import Post, Comment


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
