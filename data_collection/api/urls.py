from django.urls import path
from .views import submit_data

urlpatterns = [
    path("submit/", submit_data, name="submit_data"),
]
