from functools import wraps
from django.db import transaction
from .service import _get_ip
from django.apps import apps


def counter(f):
    @wraps(f)
    def decorator(request, *args, **kwargs):
        with transaction.atomic():
            PostViews = apps.get_model('posts', 'PostViews')
            PostViews.objects.get_or_create(
                post=object,
                ip=_get_ip(request)
            )
        return f(request, *args, **kwargs)
    return decorator