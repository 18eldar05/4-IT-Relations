from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'reading_room']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}
        }

    def save(self):
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"email": ["A user with that email already exists."]})

        account = User(**self.validated_data)
        account.set_password(self.validated_data['password'])
        account.save()

        return account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'reading_room', 'pk']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}
        }


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']
