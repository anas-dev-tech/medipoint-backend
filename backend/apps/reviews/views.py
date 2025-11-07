from rest_framework.viewsets import ModelViewSet

from apps.doctors.models import Doctor
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsReviewOwnerOrReadOnly, IsCommentOwner
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound

class ReviewsViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly]

    
    def get_queryset(self):
        if self.kwargs.get("doctor_pk"):                
            return super().get_queryset().filter(doctor_id=self.kwargs.get("doctor_pk"))
            
            
        return super().get_queryset()

    def perform_create(self, serializer):
        doctor_id = self.kwargs.get("doctor_pk")
        if doctor_id:
           doctor = get_object_or_404(Doctor, pk=doctor_id)
           serializer.save(patient=self.request.user.patient, doctor=doctor)
        else:
            raise NotFound("Doctor not found for creating review.")


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentOwner]

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_pk")
        review = get_object_or_404(Review, pk=review_id)       
        serializer.save(user=self.request.user, review=review, type=self.request.user.role)

    def get_queryset(self):
        review_id = self.kwargs.get("review_pk")
        if review_id:
            return self.queryset.filter(review_id=review_id)
        
        return self.queryset
