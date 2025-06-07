from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.api.models import FitnessClass, Booking


class Command(BaseCommand):
    help = 'Seed demo fitness classes'

    def handle(self, *args, **options):

        Booking.objects.all().delete()
        FitnessClass.objects.all().delete()

        now = timezone.now()
        classes = [
            {'name': 'Yoga', 'datetime': now + timedelta(days=1), 'instructor': 'Anu', 'available_slots': 10},
            {'name': 'Zumba', 'datetime': now + timedelta(days=2), 'instructor': 'Ria', 'available_slots': 15},
            {'name': 'Pilates', 'datetime': now + timedelta(days=3), 'instructor': 'Sam', 'available_slots': 12},
        ]
        for c in classes:
            FitnessClass.objects.create(**c)
        self.stdout.write(self.style.SUCCESS('Demo fitness classes created.'))
