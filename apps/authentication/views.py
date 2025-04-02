from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, ProfilePhotoSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from .models import SecurityLog
from .serializers import SecurityLogSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario registrado exitosamente."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Puedes agregar más datos al token si quieres
        token['email'] = user.email
        token['name'] = user.first_name
        return token

    def validate(self, attrs):
        attrs['username'] = attrs.get('email')  # usa email como username
        return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "comuna": user.comuna,  # 👈 Asegúrate de incluir esto
            "photoURL": request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
        })

    
class UpdateProfilePhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ProfilePhotoSerializer(data=request.data)
        if serializer.is_valid():
            request.user.profile_picture = serializer.validated_data['profile_picture']
            request.user.save()
            return Response({
                'photoURL': request.build_absolute_uri(request.user.profile_picture.url)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not user.check_password(current_password):
            return Response({"error": "La contraseña actual es incorrecta"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        SecurityLog.objects.create(user=user, action="Cambio de contraseña")

        return Response({"message": "Contraseña actualizada correctamente"}, status=status.HTTP_200_OK)

class SecurityLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = SecurityLog.objects.filter(user=request.user).order_by('-timestamp')
        serializer = SecurityLogSerializer(logs, many=True)
        return Response(serializer.data)