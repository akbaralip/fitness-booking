from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils.timezone import localtime

class FitnessClassSerializer(serializers.ModelSerializer):
    datetime = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = '__all__'

    def get_datetime(self, obj):
        return localtime(obj.datetime).strftime('%d-%m-%Y %I:%M %p')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'