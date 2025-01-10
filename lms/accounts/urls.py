from django.urls import path
from . import views
urlpatterns = [
    path("change-email/", views.CustomConfirmEmailView.as_view(), name="change-email")
]
