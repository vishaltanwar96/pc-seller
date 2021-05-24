from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken

from users.serializers import UserSerializer, CustomAuthTokenSerializer

User = get_user_model()


class RegistrationView(APIView):

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        User.objects.create_user(**serializer.validated_data)
        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):

    serializer_class = CustomAuthTokenSerializer
