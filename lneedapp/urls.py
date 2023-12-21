from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserProfileAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('Profile/', UserProfileAPIView.as_view(), name='user-Profile'),

]
