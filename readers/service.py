from .models import Reader, Comment
from django.contrib import messages


def add_comment(request, post, **kwargs) -> None:
    commentator, created = Reader.objects.get_or_create(
        email=kwargs['email']
    )
    commentator.name = kwargs['name']
    commentator.save()

    Comment.objects.create(
        post=post,
        commentator=commentator,
        text=kwargs['text']
    )

    messages.add_message(request, messages.SUCCESS, 'Комментарий успешно добавлен!')