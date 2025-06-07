# 🏋️ Fitness Booking API

A simple Django REST API for booking fitness classes.

## 📦 Setup

```bash
git clone <repo-url>
cd fitness_booking
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver

API Endpoints

🔹GET /api/classes/
Success Response:
[
  {
    "id": 1,
    "name": "Yoga",
    "datetime": "2025-06-10T06:30:00Z",
    "instructor": "Akku",
    "available_slots": 10
  },
  ...
]

🔹POST /api/book-class/
Request Body (JSON):
{
  "class_id": 2,
  "client_name": "Basi",
  "client_email": "basi@example.com",
}
Success Response:
{
    "client_name": "Basi",
    "client_email": "basi@example.com",
    "class_id": 2
}

🔹 GET /api/bookings?email=basi@example.com
Success Response:
[
    {
        "id": 8,
        "fitness_class": {
            "id": 2,
            "datetime": "08-06-2025 08:01 AM",
            "name": "Yoga Class",
            "instructor": "Lalu",
            "available_slots": 16
        },
        "client_name": "Basi",
        "client_email": "basi@example.com"
    }
]

