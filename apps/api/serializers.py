from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils.timezone import localtime
from django.utils import timezone
from django.db import transaction

class FitnessClassSerializer(serializers.ModelSerializer):
    datetime = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = '__all__'

    def get_datetime(self, obj):
        return localtime(obj.datetime).strftime('%d-%m-%Y %I:%M %p')

class BookClassSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(write_only=True)
    client_name = serializers.CharField()
    client_email = serializers.EmailField()

    class Meta:
        model = Booking
        fields = ['class_id', 'client_name', 'client_email']

    def validate_client_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")
        return value

    def validate_class_id(self, value):
        try:
            fitness_class = FitnessClass.objects.get(id=value)
        except FitnessClass.DoesNotExist:
            raise serializers.ValidationError("Class not found")

        if fitness_class.datetime < timezone.now():
            raise serializers.ValidationError("Cannot book past classes")

        # Only store the ID, fetch fresh with lock later
        self.context['fitness_class_id'] = fitness_class.id
        return value

    def create(self, validated_data):
        fitness_class_id = self.context['fitness_class_id']

        with transaction.atomic():
            fitness_class = FitnessClass.objects.select_for_update().get(id=fitness_class_id)

            if fitness_class.available_slots <= 0:
                raise serializers.ValidationError("No slots available")

            booking = Booking.objects.create(
                fitness_class=fitness_class,
                client_name=validated_data['client_name'],
                client_email=validated_data['client_email']
            )
            fitness_class.available_slots -= 1
            fitness_class.save()
            return booking

class BookingsSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'