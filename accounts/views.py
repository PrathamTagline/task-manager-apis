from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from accounts.models import User
from .serializers import (
    SignupSerializer,
    ForgotPasswordSerializer,
    SigninTokenObtainPairSerializer,
    UserSerializer,
    ProfileSerializer,
)
from rest_framework_simplejwt.views import TokenVerifyView as SimpleJWTTokenVerifyView


class SigninView(TokenObtainPairView):
    serializer_class = SigninTokenObtainPairSerializer


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenVerificationView(SimpleJWTTokenVerifyView):
    permission_classes = [AllowAny]


class UserDataSetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersDataViaEmailAndPattern(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        email_pattern = self.request.query_params.get('email_pattern')
        if email:
            return User.objects.filter(email=email)

        if email_pattern:
            return User.objects.filter(email__icontains=email_pattern)

        return User.objects.none()


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def signin_page_view(request):
    return render(request, 'accounts/signin_page.html')


def signup_page_view(request):
    return render(request, 'accounts/signup_page.html')


def profile_page_view(request):
    return render(request, 'accounts/profile_page.html')
