from django.urls import path
from .views import AnonymousReportCreateView, ReportListView, ReportReviewToggleView, ReporteListCreateView, ReporteCreateView

urlpatterns = [
    path('submit/', AnonymousReportCreateView.as_view(), name='submit-anonymous-report'),
    path('admin/list/', ReportListView.as_view(), name='report-list'),
    path('admin/<int:pk>/toggle/', ReportReviewToggleView.as_view(), name='toggle-review'),
    path('reportes/', ReporteCreateView.as_view(), name='crear-reporte'),
]
