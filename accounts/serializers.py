from .models import User

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer

from django.contrib.auth.password_validation import validate_password


class SigninTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['password'] = user.password

        return token


class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'password2', 'profile_image']
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'email': {'validators': [UniqueValidator(queryset=User.objects.all())]},
            'profile_image': {'required': False, 'allow_null': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        profile_image = validated_data.pop('profile_image', None)
        user = User.objects.create_user(**validated_data)
        if profile_image:
            user.profile_image = profile_image
            user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = self.user  # Use the stored user from validation

        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construct password reset link with proper format
        reset_link = f"http://127.0.0.1:8000/api/reset-password/{uid}/{token}/"

        try:
            # Send email
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link below to reset your password:\n{reset_link}",
                from_email="prathamp.tagline@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            raise serializers.ValidationError(
                f"Failed to send email: {str(e)}")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'profile_image', 'phone', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Handle profile image upload separately if needed
        profile_image = validated_data.pop('profile_image', None)
        if profile_image:
            instance.profile_image = profile_image

        return super().update(instance, validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','profile_image','phone','address']
        read_only_fields = ['email']

    def update(self, instance, validated_data):
        # Handle profile image update
        profile_image = validated_data.pop('profile_image', None)
        if profile_image:
            instance.profile_image = profile_image

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
