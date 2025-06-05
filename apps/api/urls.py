from django.urls import path
from .views import *

urlpatterns = [
    path('classes/', FitnessClassListing.as_view()),
]