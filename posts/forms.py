from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Post
from django import forms


class PostOverrideForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditorUploadingWidget(config_name='default'), label='Текст')

    class Meta:
        model = Post
        fields = '__all__'