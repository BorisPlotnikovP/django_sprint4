from django.contrib.auth import get_user_model
from django.db import models

from core.constants import DISPLAY_CHARS, MAX_FIELD_LEN
from core.models import DefaultModel

User = get_user_model()


class Location(DefaultModel):
    name = models.CharField(
        max_length=MAX_FIELD_LEN,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:DISPLAY_CHARS]


class Category(DefaultModel):
    title = models.CharField(
        max_length=MAX_FIELD_LEN,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title[:DISPLAY_CHARS]


class Post(DefaultModel):
    title = models.CharField(
        max_length=MAX_FIELD_LEN,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='posts_images',
        blank=True
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = (
            '-pub_date',
        )

    def __str__(self) -> str:
        return self.title[:DISPLAY_CHARS]


class Comment(models.Model):
    text = models.TextField('Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время публикации'
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.text[:DISPLAY_CHARS]} | {self.post} | {self.author}'
