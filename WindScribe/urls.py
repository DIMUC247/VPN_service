from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.get_subscribtions_view, name="subscriptions"),
]