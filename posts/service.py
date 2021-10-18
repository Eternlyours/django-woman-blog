from django.apps import apps


def add_views(object, request) -> None:
    PostViews = apps.get_model('posts', 'PostViews')
    PostViews.objects.get_or_create(
        post=object,
        ip=_get_ip(request)
    )


def _get_ip(request):
    try:
        forward = request.META.get('HTTP_X_FORWARDED_FOR')
        if forward:
            ip = forward.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip = ''
    return ip
