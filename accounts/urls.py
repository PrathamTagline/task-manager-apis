from django.urls import path
from .views import (
    SigninView,
    SignupView,
    ForgotPasswordView,
    UserDataSetView,
    TokenVerificationView,
    LogoutView,
)

urlpatterns = [
    path('signin/', SigninView.as_view(), name='signin'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('user/', UserDataSetView.as_view(), name='user_data_set'),
    path('token/verify/', TokenVerificationView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
]