from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (
    DetailView, ListView, CreateView, DeleteView
)
from django.views.generic.edit import UpdateView

from core.constants import DISPLAY_COUNT
from .forms import PostForm, ProfileUpdateForm, CommentForm
from .models import Post, Category, Comment

User = get_user_model()


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


def get_post_list():
    return (
        Post.objects.select_related('category', 'author', 'location')
    )


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = get_post_list().filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )
    paginate_by = DISPLAY_COUNT


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True
        ),
        slug=category_slug
    )
    post_list = (
        category.posts
        .select_related(
            'category',
            'author',
            'location'
        )
        .filter(
            pub_date__lte=timezone.now(),
            is_published=True
        )
    )
    paginator = Paginator(post_list, DISPLAY_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'post_list': post_list,
        'page_obj': page_obj
    }
    return render(request, template_name, context)


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f'/profile/{self.request.user.username}/'


class PostEditView(PermissionTestMixin, PostMixin, UpdateView):
    form_class = PostForm

    def get_success_url(self):
        return f'/posts/{self.kwargs["post_id"]}/'

    def handle_no_permission(self):
        return redirect(self.get_success_url())


class PostDeleteView(PermissionTestMixin, PostMixin, DeleteView):
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.get_object())
        return context


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_object(self):
        post = get_object_or_404(
            get_post_list(),
            pk=self.kwargs['post_id']
        )
        if (
            (post.is_published and post.category.is_published
             and post.pub_date <= timezone.now()
             )
            or post.author == self.request.user
        ):
            return post
        else:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentUpdateView(PermissionTestMixin, CommentMixin, UpdateView):
    form_class = CommentForm

    def get_success_url(self):
        return f'/posts/{self.kwargs.get("post_id")}'


class CommentDeleteView(PermissionTestMixin, CommentMixin, DeleteView):
    context_object_name = 'comment'

    def get_success_url(self):
        return f'/posts/{self.kwargs.get("post_id")}'


def profile(request, username):
    user = get_object_or_404(
        User,
        username=username
    )
    post_list = get_post_list().filter(author=user)
    paginator = Paginator(post_list, DISPLAY_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'profile': user
    }
    return render(request, 'blog/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    model = User
    template_name = 'blog/user.html'

    def get_success_url(self):
        return f'/profile/{self.request.user.username}/'

    def get_object(self):
        return self.request.user
