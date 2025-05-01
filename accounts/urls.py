from django.urls import path
from .views import (
    SigninView,
    SignupView,
    ForgotPasswordView,
    UserDataSetView,
    TokenVerificationView,
    LogoutView,
    UsersDataViaEmailAndPattern,
    profile_page_view,
    signin_page_view,
    signup_page_view,
)

urlpatterns = [
    # API views
    path('api/signin/', SigninView.as_view(), name='signin'),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('api/user/', UserDataSetView.as_view(), name='user_data_set'),
    path('api/user/search/', UsersDataViaEmailAndPattern.as_view(), name='user_data_set_search'),
    path('api/token/verify/', TokenVerificationView.as_view(), name='token_verify'),
    path('api/logout/', LogoutView.as_view(), name='logout'),


     path('signin/', signin_page_view, name='signin_page'),
    path('signup/', signup_page_view, name='signup_page'),
    path('profile/', profile_page_view, name='profile_page'),
]