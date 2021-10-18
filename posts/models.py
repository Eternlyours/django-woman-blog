from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.utils.functional import cached_property
from .managers import PostManager


class Post(models.Model):
    slug = models.SlugField('Семантический URL')
    title = models.CharField('Заголовок', max_length=255, unique=True)
    body = models.TextField('Текст')
    is_active = models.BooleanField('Отображать на сайте', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата редактирования', auto_now=True)
    meta_description = models.TextField('Мета описание')
    meta_keywords = models.TextField('Мета ключевые слова')
    picture_for_header = models.ImageField(
        'Картинка для заголовка', upload_to='uploads/posts/headers/%y/%m/%d/')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post', verbose_name='Автор')
    rubric = models.ForeignKey(
        'Rubric', on_delete=models.CASCADE, related_name='posts', verbose_name='Рубрика'
    )

    objects = PostManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'Публикация - {self.title}'

    @cached_property
    def get_views(self):
        return self.views.count()
    get_views.short_description = 'Количество просмотров'

    @cached_property
    def get_next_post(self):
        post = Post.objects.filter(
            is_active=True, created_at__gt=self.created_at).order_by('created_at').values('slug', 'title', 'picture_for_header').first()
        if post is None:
            post = Post.objects.order_by('created_at').values('slug', 'title', 'picture_for_header').first()
        return post

    @cached_property
    def get_previous_post(self):
        post = Post.objects.filter(
            is_active=True, created_at__lt=self.created_at).order_by('created_at').values('slug', 'title', 'picture_for_header').first()
        if post is None:
            post = Post.objects.order_by('-created_at').values('slug', 'title', 'picture_for_header').first()
        return post

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Rubric(models.Model):
    slug = models.SlugField('Семантический URL')
    title = models.CharField('Название', max_length=255, unique=True)
    description = models.CharField('Описание', max_length=255)
    meta_description = models.TextField('Мета описание')
    meta_keywords = models.TextField('Мета ключевые слова')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'Рубрика - {self.title}'

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'


class PostViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='views', verbose_name='Публикация')
    ip = models.GenericIPAddressField(verbose_name='IP читателя')

    def __str__(self) -> str:
        return f'Просмотр ip - {self.ip}'

    class Meta:
        verbose_name = 'Количество просмотров'
        verbose_name_plural = 'Количество просмотров'
