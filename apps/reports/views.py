from rest_framework import generics, permissions
from .models import AnonymousReport
from .serializers import AnonymousReportSerializer
from rest_framework.permissions import IsAdminUser


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