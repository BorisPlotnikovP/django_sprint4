from django.contrib import admin

from .models import Category, Location, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'description',
        'slug',
    )
    list_display_links = (
        'title',
    )
    list_editable = (
        'is_published',
        'description',
        'slug',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'is_published',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    search_fields = (
        'name',
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'is_published',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'pub_date',
        'location',
        'category',
    )
    search_fields = (
        'title',
        'category',
    )
    list_editable = (
        'is_published',
        'pub_date',
        'location',
        'category',
    )
    list_filter = (
        'is_published',
        'category',
        'location',
    )
    search_fields = (
        'title',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'post',
        'created_at',
    )
    search_fields = (
        'text',
    )
    list_editable = (
        'text',
    )
    list_filter = (
        'author',
        'post',
    )
