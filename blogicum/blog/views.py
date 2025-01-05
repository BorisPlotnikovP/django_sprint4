from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.views.generic.edit import UpdateView

from core.constants import DISPLAY_COUNT
from core.mixins import (CommentMixin, PermissionTestMixin, PostMixin,
                         PostUrlMixin, UserUrlMixin)
from core.utils import (get_page_object, get_post_list, posts_for_display,
                        count_and_order)
from .forms import CommentForm, PostForm, ProfileUpdateForm
from .models import Category, Post

User = get_user_model()


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = count_and_order(posts_for_display())
    paginate_by = DISPLAY_COUNT


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects
        .filter(
            is_published=True
        ),
        slug=category_slug
    )
    post_list = count_and_order(posts_for_display().filter(category=category))
    context = {
        'category': category,
        'page_obj': get_page_object(request, post_list, DISPLAY_COUNT)
    }
    return render(request, 'blog/category.html', context)


class PostCreateView(LoginRequiredMixin, UserUrlMixin, PostMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, PermissionTestMixin, PostMixin,
                   PostUrlMixin, UpdateView):
    form_class = PostForm

    def handle_no_permission(self):
        return redirect(self.get_success_url())


class PostDeleteView(LoginRequiredMixin, PermissionTestMixin, PostMixin,
                     DeleteView):
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.get_object())
        return context


class PostDetailView(LoginRequiredMixin, PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_object(self):
        post = get_object_or_404(
            get_post_list()
            .filter(
                (
                    Q(is_published=True)
                    & Q(category__is_published=True)
                    & Q(pub_date__lte=timezone.now())
                ) | Q(author=self.request.user)
            ),
            pk=self.kwargs['post_id'],
        )
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
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


class CommentUpdateView(LoginRequiredMixin, PermissionTestMixin, PostUrlMixin,
                        CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(PermissionTestMixin, PostUrlMixin, CommentMixin,
                        DeleteView, LoginRequiredMixin):
    context_object_name = 'comment'


def profile(request, username):
    user = get_object_or_404(
        User,
        username=username
    )
    if request.user == user:
        post_list = count_and_order(get_post_list().filter(author=user))
    else:
        post_list = count_and_order(posts_for_display().filter(author=user))
    context = {
        'page_obj': get_page_object(request, post_list, DISPLAY_COUNT),
        'profile': user
    }
    return render(request, 'blog/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UserUrlMixin, UpdateView):
    form_class = ProfileUpdateForm
    model = User
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user
