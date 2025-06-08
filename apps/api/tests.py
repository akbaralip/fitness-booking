from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from .models import FitnessClass

class BookingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fitness_class = FitnessClass.objects.create(
            name="Test Yoga",
            datetime=timezone.now() + timezone.timedelta(days=1),
            instructor="Akku",
            available_slots=1
        )

    def test_successful_booking(self):
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "Alice",
            "client_email": "alice@example.com"
        }
        response = self.client.post("/api/book-class/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["client_name"], "Alice")

    def test_overbooking_not_allowed(self):
        # First booking
        self.client.post("/api/book-class/", {
            "class_id": self.fitness_class.id,
            "client_name": "Alice",
            "client_email": "alice@example.com"
        }, format="json")

        # Second booking - should fail
        response = self.client.post("/api/book-class/", {
            "class_id": self.fitness_class.id,
            "client_name": "Bob",
            "client_email": "bob@example.com"
        }, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("No slots available", str(response.data))
