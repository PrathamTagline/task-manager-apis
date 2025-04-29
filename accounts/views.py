from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    SignupSerializer,
    ForgotPasswordSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenVerifySerializer,
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
        email = request.query_params.get('email', None)
        email_pattern = request.query_params.get('email_pattern', None)

        if email and email_pattern:
            users = UserSerializer.Meta.model.objects.filter(
                email__iexact=email, email__istartswith=email_pattern
            )
        elif email:
            users = UserSerializer.Meta.model.objects.filter(email__iexact=email)
        elif email_pattern:
            users = UserSerializer.Meta.model.objects.filter(email__istartswith=email_pattern)
        else:
            return Response({"error": "At least one of 'email' or 'email_pattern' is required."}, status=status.HTTP_400_BAD_REQUEST)

        if users.exists():
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No users found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)
    

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