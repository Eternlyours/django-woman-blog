from readers.models import Comment, Reader
from django.contrib import admin


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    fields = ('email', 'name', 'date_join', )
    readonly_fields = ('email', 'name', 'date_join', )
    list_display = ('email', 'name', 'date_join', )
    list_display_links = ('email', 'name', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass