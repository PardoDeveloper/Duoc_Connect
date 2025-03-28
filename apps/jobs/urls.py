from django.urls import path
from .views import JobOfferListCreateView, ApplyToJobView

urlpatterns = [
    path('offers/', JobOfferListCreateView.as_view(), name='job-offers'),
    path('offers/<int:offer_id>/apply/', ApplyToJobView.as_view(), name='apply-job'),
]
