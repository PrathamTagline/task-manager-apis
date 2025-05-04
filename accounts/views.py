from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from accounts.models import User
from .serializers import (
    SignupSerializer,
    ForgotPasswordSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
)
from rest_framework_simplejwt.views import TokenVerifyView as SimpleJWTTokenVerifyView


class SigninView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class TokenVerificationView(SimpleJWTTokenVerifyView):
    permission_classes = [AllowAny]

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


class UserDataSetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        user = request.user
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No users found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)
    


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
        

        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token to log out the user
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



    
def signin_page_view(request):
   return render(request, 'accounts/signin_page.html')

def signup_page_view(request):
   return render(request, 'accounts/signup_page.html')       

def profile_page_view(request):
   return render(request, 'accounts/profile_page.html')
