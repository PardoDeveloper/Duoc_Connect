from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, UserProfileView, UpdateProfilePhotoView, ChangePasswordView, SecurityLogView

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/photo/', UpdateProfilePhotoView.as_view(), name='update-profile-photo'),
    path('profile/password/', ChangePasswordView.as_view(), name='change-password'),
    path('security/logs/', SecurityLogView.as_view(), name='security-logs'),
    
    # path('profile/password/', ChangePasswordView.as_view(), name='change-password'),  # si usas el cambio de contraseña
    # path('auth/profile/photo/', UpdateProfilePhotoView.as_view(), name='update-profile-photo'),

]
