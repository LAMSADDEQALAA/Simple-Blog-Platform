from django.urls import path
from .views import UserRegistrationView,UserDetailView,UsersByIdsView
from rest_framework_simplejwt.views import  TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('', UsersByIdsView.as_view(), name='users_by_ids'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]