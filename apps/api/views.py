from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email
from rest_framework.views import APIView
from .models import FitnessClass, Booking
from django.utils.timezone import now
from .serializers import FitnessClassSerializer, BookClassSerializer, BookingsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

# Create your views here.
class FitnessClassListing(APIView):
    def get(self, request):
        classes = FitnessClass.objects.filter(datetime__gte=now()).order_by('datetime')
        serializer = FitnessClassSerializer(classes, many=True)
        return Response(serializer.data)


class BookClass(APIView):
    def post(self, request):
        serializer = BookClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = serializer.data
            response['class_id'] = request.data.get('class_id')
            return Response(response, status=201)
        return Response({'error': serializer.errors}, status=400)


class Bookings(APIView):
    def get(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email format'}, status=400)

        bookings = Booking.objects.filter(client_email=email)
        if not bookings.exists():
            return Response({'message': 'No bookings found for this email'}, status=200)

        serializer = BookingsSerializer(bookings, many=True)
        return Response(serializer.data)

