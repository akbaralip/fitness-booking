from rest_framework.views import APIView
from .models import FitnessClass, Booking
from django.utils.timezone import now
from .serializers import FitnessClassSerializer, BookingSerializer
from rest_framework.response import Response

# Create your views here.
class FitnessClassListing(APIView):
    def get(self, request):
        classes = FitnessClass.objects.filter(datetime__gte=now()).order_by('datetime')
        serializer = FitnessClassSerializer(classes, many=True)
        return Response(serializer.data)

