from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StudyGroup, GroupMembership, SharedFile
from .serializers import StudyGroupSerializer, GroupMembershipSerializer, SharedFileSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class StudyGroupListCreateView(generics.ListCreateAPIView):
    queryset = StudyGroup.objects.all().order_by('-created_at')
    serializer_class = StudyGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class JoinGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, group_id):
        group = StudyGroup.objects.get(pk=group_id)
        membership, created = GroupMembership.objects.get_or_create(
            group=group,
            user=request.user
        )
        if not created:
            return Response({'message': 'Ya estás en este grupo'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Te uniste al grupo con éxito'}, status=status.HTTP_201_CREATED)


class LeaveGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, group_id):
        try:
            membership = GroupMembership.objects.get(group_id=group_id, user=request.user)
            membership.delete()
            return Response({'message': 'Saliste del grupo'}, status=status.HTTP_200_OK)
        except GroupMembership.DoesNotExist:
            return Response({'message': 'No perteneces a este grupo'}, status=status.HTTP_400_BAD_REQUEST)

class SharedFileListCreateView(generics.ListCreateAPIView):
    serializer_class = SharedFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # para aceptar archivos

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return SharedFile.objects.filter(group_id=group_id).order_by('-uploaded_at')

    def perform_create(self, serializer):
        group_id = self.kwargs['group_id']
        serializer.save(uploaded_by=self.request.user, group_id=group_id)