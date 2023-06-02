from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import authenticate
from users.models import User, Profile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email  # 확장
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class UserSerializerWithToken(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('email', 'password')


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        print(data)
        user = authenticate(**data)
        if user:
            set_token = MyTokenObtainPairSerializer.get_token(user)
            token = {
                'refresh': str(set_token),
                'access': str(set_token.access_token)
            }
            return {'email': user.email, 'token': token}
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."})


class ProfileSerializer(serializers.ModelSerializer):
    # 유저의 프로필을 색인 작업할 pk값 입력받기. 추후 닉네임 부분 수정 부분 추가.1111333222322442
    class Meta:
        model = Profile
        fields = "__all__"