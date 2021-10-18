from django import forms
from typing import Dict, Any
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.Form):
    text = forms.CharField(label='Комментарий', widget=CKEditorWidget('comment'))
    name = forms.CharField(label='Имя', max_length=100)
    email = forms.EmailField(label='Электронная почта', validators=[EmailValidator], help_text='Ваш адрес email не будет опубликован.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'comment-form-fields'

    def clean(self) -> Dict[str, Any]:
        data = self.cleaned_data
        if data['name'] == '1':
            self.add_error('name', 'Ошибка')
        return data