from django.apps import apps
from django.db.models import F, Manager, Q
from django.db.models.aggregates import Count, Sum
from django.db.models.expressions import ExpressionWrapper, OuterRef, Subquery
from django.db.models.fields import IntegerField
from django.db.models.query import Prefetch


class PostManager(Manager):
    def get_list_view_posts(self):
        PostViews = apps.get_model('posts', 'PostViews')

        posts = self.all().select_related(
            'rubric'
        )
        # .prefetch_related(
        #     Prefetch(
        #         'views',
        #         queryset=PostViews.objects.all()
        #     )
        # )
        # .annotate(
        #     number_views = Count('views')
        # )
        return posts
