from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from users.permissions import IsAdminUser
from users.serializers import (
    LogoutSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserRoleUpdateSerializer,
)


User = get_user_model()


class UserRegisterView(APIView):
    """
    Register a new user and return JWT tokens.
    """
    permission_classes = []
    
    def post(self, request: Request, format: str = "json") -> Response:
        serializer = UserSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)
        
        return Response(response, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    Custom login view that returns user details along with tokens.
    """
    permission_classes = []
    
    def post(self, request: Request) -> Response:
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=email, password=password)
        
        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {"error": "User account is disabled"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    """
    Logout user by blacklisting their refresh token.
    """
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)
    
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListView(generics.ListAPIView):
    """
    List all users (admin only).
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user (admin only).
    Can update role (is_staff) and profile info.
    """
    permission_classes = (IsAdminUser,)
    lookup_field = "id"
    queryset = User.objects.all()
    
    def get_serializer_class(self):  # type: ignore[no-untyped-def]
        if self.request.method in ['PUT', 'PATCH']:
            return UserRoleUpdateSerializer
        return UserSerializer

class UserMeView(APIView):
    """
    Get or update current user profile.
    Regular users can only update their name, not their role.
    """
    permission_classes = (IsAuthenticated,)
    
    def get(self, request: Request) -> Response:
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request: Request) -> Response:
        serializer = UserUpdateSerializer(
            request.user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    