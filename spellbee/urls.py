from django.urls import path
from . import views

urlpatterns = [
    path("refresh/", views.RefreshLetters.as_view(), name='refresh-letters'),
    path("validate/", views.ValidateInput.as_view(), name='validate-word'),
]