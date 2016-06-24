from django.conf.urls import url
from .views import register, registered, courses, registered_dates

urlpatterns = [
    url(r'^register/(\d+)$', register, name="register"),
    url(r'^registered/(\d+)/(\d{4}-\d{2}-\d{2})$', registered, name="registered"),
    url(r'^registered-dates/(\d+)$', registered_dates, name="registered-dates"),
    url(r'^courses$', courses, name="courses"),
]
