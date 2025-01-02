from django.urls import include, path

from . import views

app_name = 'blog'

posts_urls = [
    path(
        route='<int:post_id>/',
        view=views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        route='create/',
        view=views.PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        route='<int:post_id>/edit/',
        view=views.PostEditView.as_view(),
        name='edit_post'
    ),
    path(
        route='<int:post_id>/delete/',
        view=views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        route='<int:post_id>/comment/',
        view=views.comment_create,
        name='add_comment'
    ),
    path(
        route='<int:post_id>/edit_comment/<int:comment_id>/',
        view=views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        route='<int:post_id>/delete_comment/<int:comment_id>/',
        view=views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
]

urlpatterns = [
    path(
        route='',
        view=views.IndexView.as_view(),
        name='index'
    ),
    path(
        route='profile/edit/',
        view=views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    path(
        route='profile/<str:username>/',
        view=views.profile,
        name='profile'
    ),
    path(
        route='category/<slug:category_slug>/',
        view=views.category_posts,
        name='category_posts'
    ),
    path(
        route='posts/',
        view=include(posts_urls)
    ),
]
