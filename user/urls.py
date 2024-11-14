from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("broadcast", views.BroadCastAPIView.as_view(), name="broadcast"),
]
