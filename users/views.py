from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from users.permissions import IsStaffOrOwner, IsAdmin
from .serializer import UserRegisterSerializer, UserSerializer, UserRoleSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()

            data['response'] = 'Account has been created'
            data['username'] = account.username
            data['email'] = account.email
            data['pk'] = account.pk
            refresh = RefreshToken.for_user(account)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)


class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsStaffOrOwner,)


class UserRoleView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = (IsAdmin,)


class AllUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
