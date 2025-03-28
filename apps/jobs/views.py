from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import JobOffer, JobApplication
from .serializers import JobOfferSerializer, JobApplicationSerializer
from django.db.models import Q


class JobOfferListCreateView(generics.ListCreateAPIView):
    serializer_class = JobOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = JobOffer.objects.all().order_by('-created_at')
        search = self.request.query_params.get('search')
        location = self.request.query_params.get('location')
        company = self.request.query_params.get('company')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
        )

        if location:
            queryset = queryset.filter(location__icontains=location)

        if company:
            queryset = queryset.filter(company__icontains=company)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class ApplyToJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, offer_id):
        job_offer = JobOffer.objects.get(pk=offer_id)
        application, created = JobApplication.objects.get_or_create(
            job_offer=job_offer,
            applicant=request.user,
            defaults={'cover_letter': request.data.get('cover_letter', '')}
        )
        if not created:
            return Response({'message': 'Ya postulaste a esta oferta.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Postulación realizada con éxito.'}, status=status.HTTP_201_CREATED)
