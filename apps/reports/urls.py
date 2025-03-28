from django.urls import path
from .views import AnonymousReportCreateView

urlpatterns = [
    path('submit/', AnonymousReportCreateView.as_view(), name='submit-anonymous-report'),
]
