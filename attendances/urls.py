from django.conf.urls import url
from .views import register, registered

urlpatterns = [
    url(r'^register/(\d+)$', register),
    url(r'^registered$', registered),
]
