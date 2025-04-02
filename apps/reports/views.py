from rest_framework import generics, permissions
from .models import AnonymousReport, Reporte
from .serializers import AnonymousReportSerializer, ReporteSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class AnonymousReportCreateView(generics.CreateAPIView):
    queryset = AnonymousReport.objects.all()
    serializer_class = AnonymousReportSerializer
    permission_classes = [permissions.AllowAny]  # Anónimo: no requiere login

class ReportListView(generics.ListAPIView):
    queryset = AnonymousReport.objects.all().order_by('-submitted_at')
    serializer_class = AnonymousReportSerializer
    permission_classes = [IsAdminUser]


class ReportReviewToggleView(generics.UpdateAPIView):
    queryset = AnonymousReport.objects.all()
    serializer_class = AnonymousReportSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        report = self.get_object()
        report.is_reviewed = not report.is_reviewed
        report.save()
        return Response({'message': f'Denuncia marcada como {"revisada" if report.is_reviewed else "no revisada"}'})
    
class ReporteListCreateView(generics.ListCreateAPIView):
    queryset = Reporte.objects.all().order_by('-fecha')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class ReporteCreateView(generics.CreateAPIView):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)