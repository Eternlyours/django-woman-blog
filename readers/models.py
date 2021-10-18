from django.db import models
from django.db.models.fields.related import ForeignKey
from posts.models import Post


class Reader(models.Model):
    email = models.EmailField(
        'Электронная почта читателя', unique=True)
    name = models.CharField('Имя', max_length=100)
    date_join = models.DateTimeField(
        'Дата первого присоединения', auto_now_add=True)

    def __str__(self) -> str:
        return f'Читатель - {self.email}'

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'


class Comment(models.Model):
    post = ForeignKey(Post, on_delete=models.CASCADE, related_name='comment', verbose_name='Публикация')
    commentator = models.ForeignKey(
        Reader, on_delete=models.CASCADE, related_name='comment', verbose_name='Комментатор')
    created_at = models.DateTimeField(
        'Дата создания комментария', auto_now_add=True)
    text = models.TextField('Текст')

    def __str__(self) -> str:
        return f'Комментарий - {self.text}'

    @classmethod
    def create(self, cls, **kwargs):
        comment = cls(**kwargs)
        return comment

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
