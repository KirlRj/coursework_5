from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserRegisterSerializer, UserSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user