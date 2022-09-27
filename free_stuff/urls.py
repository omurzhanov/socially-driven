from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('<int:pk>/', views.post_detail, name='post-detail'),
    path('create-post/', views.create_post, name='create-post'),
    path('edit/<int:pk>/', views.UpdatePostView.as_view(), name='edit-post'),
    path('<int:pk>/delete/', views.DeletePostView.as_view(), name='delete-post'),
]