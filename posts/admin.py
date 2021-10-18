from django.contrib import admin
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from posts.forms import PostOverrideForm
from posts.models import Post, PostViews, Rubric


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    save_on_top = True
    fields = ('slug', 'title', 'author', 'rubric', 'get_views', 'is_active', 'created_at',
              'updated_at', 'picture_for_header', 'body', 'meta_description', 'meta_keywords', )
    readonly_fields = ('slug', 'author', 'created_at',
                       'updated_at', 'get_views', )
    list_display = ('title', 'author', 'rubric', 'get_count_views', )
    sortable_by = ('get_count_views', 'author', 'rubric', )
    list_display_links = ('title', )
    list_filter = ('rubric__title', 'is_active', 'author__username', )
    date_hierarchy = 'created_at'
    form = PostOverrideForm

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        return queryset.all().prefetch_related('views').annotate(count_views=Count('views'))

    def get_count_views(self, obj):
        return obj.count_views
    get_count_views.short_description = 'Количество просмотров'
    get_count_views.admin_order_field = 'count_views'
    get_count_views.empty_value = '???'

    def save_model(self, request, obj, form, change) -> None:
        if not change:
            obj.author = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    fields = ('slug', 'title', 'description',
              'meta_description', 'meta_keywords', )
    readonly_fields = ('slug', )


@admin.register(PostViews)
class Views(admin.ModelAdmin):
    pass
