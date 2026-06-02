AUTH_PAYLOAD = {
    "username": "admin",
    "password": "password123"
}

NEW_BOOKING_DATA = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-01-01",
        "checkout": "2026-01-05"
    }
}

UPDATE_BOOKING_DATA = {
    "firstname": "Updated",
    "lastname": "Doe",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-01-01",
        "checkout": "2026-01-05"
    }
}

PATCH_BOOKING_DATA = {
    "totalprice": 200
}
