from .views import (
    DoctorViewSets,
    ScheduleViewSet,
    WorkingHoursViewSet,
    SpecialtyListAPIView,
)
from apps.reviews.views import ReviewsViewSet

from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()


router.register(r"doctors", DoctorViewSets, basename="doctors")
router.register(r"schedules", ScheduleViewSet, basename="schedules")
router.register(r"working-hours", WorkingHoursViewSet, basename="working-hours")
nested_doctor_router = NestedSimpleRouter(router, r"doctors", lookup="doctor")


nested_doctor_router.register(
    r"working-hours", WorkingHoursViewSet, basename="doctor-working-hours"
)
nested_doctor_router.register(
    r"reviews", ReviewsViewSet, basename="doctor-reviews"
)

doctor_routes = [
    path("", include(router.urls)),
    path("", include(nested_doctor_router.urls)),
    path("specialties/", SpecialtyListAPIView.as_view()),
]
