from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.find_or_create_contact),
]

if settings.DEBUG:
    urlpatterns += [path('gettoken', views.get_access_and_refresh_tokens)]

