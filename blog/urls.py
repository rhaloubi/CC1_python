from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CategoryView
)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category-detail'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
] 