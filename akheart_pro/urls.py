from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from fundraiser.views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('fundraiser/', include('fundraiser.urls')),
    path('account/', include('account.urls')),
    path('free_stuff/', include('free_stuff.urls')),
    path('petitions/', include('petition.urls')),
    path('volunteering/', include('volunteering.urls')),
    path('', home, name='home'),
    path('paypal/', include('paypal.standard.ipn.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)