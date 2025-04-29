from .models import User

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer

from django.contrib.auth.password_validation import validate_password


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['password'] = user.password

        return token
    
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2', 'profile_image']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 as it's not needed for user creation
        profile_image = validated_data.pop('profile_image', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        if profile_image:
            user.profile_image = profile_image  # Corrected field name to match 'profile_image'
            user.save()
        return user

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construct password reset link (example URL, adjust as needed)
        reset_link = f"http://example.com/reset-password/{uid}/{token}/"

        # Send email
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link below to reset your password:\n{reset_link}",
            from_email="prathamp.tagline@gmail.com",
            recipient_list=[email],
        )

class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        # Call the parent class's validate method to perform the default validation
        data = super().validate(attrs)

        # Add any custom validation or additional data if needed
        # For example, you can include a custom message or additional claims
        data['message'] = "Token is valid."

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_iamge', 'phone', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Handle profile image upload separately if needed
        profile_image = validated_data.pop('profile_iamge', None)
        if profile_image:
            instance.profile_iamge = profile_image
        
        return super().update(instance, validated_data)