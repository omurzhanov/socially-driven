from django.urls import path

from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event-list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('create/', views.create_event, name='create-event'),
    path('<int:pk>/add-skill/', views.add_skill, name='add-skill'),
    path('<int:pk>/apply/', views.apply_to_event, name='apply-event'),
    path('<int:pk>/delete/', views.DeleteEventView.as_view(), name='delete-event'),
]