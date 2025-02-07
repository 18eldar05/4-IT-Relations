from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegistrationView, UserView, UserRoleView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name="token"),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    path('api/register/', RegistrationView.as_view(), name="register"),
    path('api/user/<int:pk>/', UserView.as_view(), name="user"),
    path('api/role/<int:pk>/', UserRoleView.as_view(), name="role"),
]
