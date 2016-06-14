from django.conf.urls import url
from .views import register, registered

urlpatterns = [
    url(r'^register/(\d+)$', register, name="register"),
    url(r'^registered/(\d+)$', registered, name="registered"),
]
