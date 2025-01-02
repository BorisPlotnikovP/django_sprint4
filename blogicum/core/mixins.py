from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from blog.models import Comment, Post


class PostMixin:
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class PermissionTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class UserUrlMixin:
    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('blog:profile', kwargs={'username': username})


class PostUrlMixin:
    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse_lazy('blog:post_detail', kwargs={'post_id': post_id})
