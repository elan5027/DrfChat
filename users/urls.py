from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)
from django.urls import path
from .views import UserView, current_user, ProfileView, LoginView


urlpatterns = [
    path('signup/', UserView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('current/', current_user),
    path('profile/', ProfileView.as_view()),
]