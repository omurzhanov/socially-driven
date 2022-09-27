from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from account.views import *

from free_stuff.views import MyPostsView, my_post_detail
from petition.views import MyPetitionsView, MyPetitionDetailView
from volunteering.views import MyEventListView, MyEventDetailView
from fundraiser.views import MyFundListView, MyFundDetailView, MyFundDeleteView, MyFundUpdateView, MyDonationListView

urlpatterns = [
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/reset_password_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('signup/', RegisterView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', change_password, name='change_password'),
    path('myprofile/', profile, name='profile'),
    path('my-posts/', MyPostsView.as_view(), name='my-posts'),
    path('my-posts/<int:pk>/', my_post_detail, name='my-post-detail'),
    path('my-petitions/', MyPetitionsView.as_view(), name='my-petitions'),
    path('my-petitions/<int:pk>/', MyPetitionDetailView.as_view(), name='my-petition-detail'),
    path('my-opportunities/', MyEventListView.as_view(), name='my-events'),
    path('my-opportunities/<int:pk>/', MyEventDetailView.as_view(), name='my-event-detail'),
    path('fundraisers/', MyFundListView.as_view(), name='my-fundraisers'),
    path('fundraisers/<int:pk>/', MyFundDetailView.as_view(), name='my-fundraiser-detail'),
    path('fundraisers/<int:pk>/delete/', MyFundDeleteView.as_view(), name='my-fundraiser-delete'),
    path('fundraisers/<int:pk>/edit/', MyFundUpdateView.as_view(), name='my-fundraiser-edit'),
    path('donations/', MyDonationListView.as_view(), name='my-donations'),
]