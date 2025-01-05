from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone
from blog.models import Post


def get_post_list():
    return (
        Post.objects.select_related('category', 'author', 'location')
    )


def get_page_object(request, object_list: list, display_count: int):
    paginator = Paginator(object_list, display_count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def posts_for_display():
    return (
        get_post_list()
        .filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    )


def count_and_order(queryset):
    result_queryset = (
        queryset
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )
    return result_queryset
