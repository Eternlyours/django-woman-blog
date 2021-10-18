import json
from readers.forms import CommentForm
from readers.models import Comment

from django.core.files.uploadedfile import InMemoryUploadedFile
from .service import add_comment
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import JsonResponse
from django.views.generic.edit import CreateView, FormMixin


class CustomFileEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, InMemoryUploadedFile):
            return o.read()
        return str(o)


class JSONResponsableFormMixin(FormMixin):

    def form_valid(self, form):
        response = json.dumps(form.cleaned_data, cls=CustomFileEncoder)
        return JsonResponse({'response': response}, status=200)

    def form_invalid(self, form):
        response = json.dumps(form.errors)
        return JsonResponse({'response': response}, status=400)


class CreateCommentView(JSONResponsableFormMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        add_comment(self.request, self.get_object, form)
        return super().form_valid(form)
