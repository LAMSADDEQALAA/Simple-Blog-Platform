from rest_framework import permissions
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from django.contrib.auth.models import User
from .serializers import UserCreateUpdateSerializer,UserSerializer
from rest_framework.response import Response


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"id": response.data["id"], "username": response.data["username"]}, status=response.status_code)
    
class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user 