from django.urls import path

from . import views

urlpatterns = [
    path('', views.PetitionListView.as_view(), name='petition-list'),
    path('<int:pk>/', views.PetitionDetailView.as_view(), name='petition-detail'),
    path('create-petition/', views.create_petition, name='create-petition'),
    path('<int:pk>/delete/', views.DeletePetitionView.as_view(), name='delete-petition'),
    path('<int:pk>/share/', views.petition_share, name='share-petition'),
]