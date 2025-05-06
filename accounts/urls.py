from django.urls import path
from .views import (
    ProfileView,
    SigninView,
    SignupView,
    ForgotPasswordView,
    UserDataSetView,
    TokenVerificationView,
    UsersDataViaEmailAndPattern,
    profile_page_view,
    signin_page_view,
    signup_page_view,
)

urlpatterns = [
    # JWT authentication APIs
    path('api/signin/', SigninView.as_view(), name='signin'),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('api/user/', UserDataSetView.as_view(), name='user_data_set'),
    path('api/user/search/', UsersDataViaEmailAndPattern.as_view(), name='user_data_set_search'),
    path('api/token/verify/', TokenVerificationView.as_view(), name='token_verify'),
    path("api/profile/", ProfileView.as_view(), name=""),

    # templates url
    path('signin/', signin_page_view, name='signin_page'),
    path('signup/', signup_page_view, name='signup_page'),
    path('profile/', profile_page_view, name='profile_page'),
]