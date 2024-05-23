from django.urls import path
from . import views

urlpatterns = [
    path("letters/refresh/", views.RefreshLetters.as_view(), name='refresh-letters'),
    path("letters/validate/", views.ValidateInput.as_view(), name='validate-word'),
]