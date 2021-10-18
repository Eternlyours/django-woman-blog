from typing import Any, Dict

from django.db.models.aggregates import Count
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, FormView
from django.views.generic.list import ListView
from readers.forms import CommentForm
from readers.models import Comment, Reader
from readers.service import add_comment

from .models import Post, Rubric
from .service import add_views


class HeaderMixin:
    def dispatch(self, request, *args, **kwargs):
        self.header = Rubric.objects.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = self.header
        return context

class PostDetail(HeaderMixin, FormView, DetailView):
    queryset = Post.objects.get_list_view_posts()
    template_name = 'posts/post-detail.html'
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse('post-detail', kwargs={'slug': self.object.slug})

    def get(self, request, *args, **kwargs):
        add_views(self.object, request)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def form_valid(self, form):
        data = form.cleaned_data
        post = self.object
        add_comment(self.request, post, **data)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(object=self.object, form=form))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().select_related(
            'commentator').filter(post=self.object).order_by('-created_at')
        context['next_post'] = self.object.get_next_post
        context['previous_post'] = self.object.get_previous_post
        return context


class HomeView(HeaderMixin, ListView):
    template_name = 'blog/index.html'
    queryset = Post.objects.get_list_view_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = self.queryset.prefetch_related('views').alias(
            views_count=Count('views')).order_by('-views_count')[:15]
        return context
