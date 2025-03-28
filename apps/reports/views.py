from rest_framework import generics, permissions
from .models import AnonymousReport
from .serializers import AnonymousReportSerializer


class AnonymousReportCreateView(generics.CreateAPIView):
    queryset = AnonymousReport.objects.all()
    serializer_class = AnonymousReportSerializer
    permission_classes = [permissions.AllowAny]  # Anónimo: no requiere login
