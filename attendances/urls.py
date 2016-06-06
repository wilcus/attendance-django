from django.conf.urls import url
from .views import register, registered

urlpatterns = [
    url(r'^register$', register),
    url(r'^registered$', registered),
]
