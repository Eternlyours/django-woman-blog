from django.urls import path
from .views import HomeView, PostDetail


urlpatterns = [
    path('posts/<slug>/', PostDetail.as_view(), name='post-detail'),
    path('', HomeView.as_view(), name='home'),
]
