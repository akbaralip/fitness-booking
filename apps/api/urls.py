from django.urls import path
from .views import *

urlpatterns = [
    path('classes/', FitnessClassListing.as_view()),
    path('book-class/', BookClass.as_view(), name='book-class'),
    path('bookings/', Bookings.as_view())
]