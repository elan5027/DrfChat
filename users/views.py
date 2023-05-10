from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Profile, User
from users.serializers import UserSerializer, ProfileSerializer, LoginSerializer, UserSerializerWithToken

from rest_framework.decorators import api_view
from .permissions import CustomReadOnly
from django.conf import settings



@api_view(['GET'])
def current_user(request):
    """
        현제 로그인 한 유저의 정보를 출력 한다.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializerWithToken(data=request.data)
        if not serializer.is_valid():
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request error"}, status=status.HTTP_409_CONFLICT)

        token = serializer.validated_data
        return Response(token, status=status.HTTP_200_OK)


class ProfileView(APIView):
    def get(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)