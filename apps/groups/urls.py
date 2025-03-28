from django.urls import path
from .views import StudyGroupListCreateView, JoinGroupView, LeaveGroupView

urlpatterns = [
    path('study-groups/', StudyGroupListCreateView.as_view(), name='study-group-list-create'),
    path('study-groups/<int:group_id>/join/', JoinGroupView.as_view(), name='join-group'),
    path('study-groups/<int:group_id>/leave/', LeaveGroupView.as_view(), name='leave-group'),
]
