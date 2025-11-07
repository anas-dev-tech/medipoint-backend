from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import AppointmentViewSet
from .webhook import stripe_webhook 
from apps.reviews.views import ReviewsViewSet

router = SimpleRouter()

router.register(r"appointments", AppointmentViewSet, basename='appointments')


appointment_routes = [
    path('', include(router.urls)),
    path('webhook/', stripe_webhook, name='appointment_payment_webhook'),
]
