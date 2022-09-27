from django.urls import path

from . import views

urlpatterns = [
    path('', views.FundListView.as_view(), name='fund-list'),
    path('<int:pk>/', views.FundDetailView.as_view(), name='fund-detail'),
    path('<int:pk>/donate/', views.donate, name='fund-donate'),
    path('<int:pk>/share/', views.fundraiser_share, name='fund-share'),
    path('create/fundraiser/', views.add_fundraiser, name='add-fundraiser'),
    path('payment/process/', views.payment_process, name='payment-process'),
    path('payment/done/<int:pk>/', views.payment_done, name='payment-done'),
    path('payment/canceled/<int:pk>/', views.payment_canceled, name='payment-canceled'),
]