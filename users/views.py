from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.permissions import IsAdminUser
from users.serializers import (
    LogoutSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserRoleUpdateSerializer,
)
from rest_framework.decorators import api_view, permission_classes
from teams.models import Team
from teams.serializers import TeamSerializer

User = get_user_model()


class UserRegisterView(APIView):
    """
    Register a new user and return JWT tokens.
    """
    
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


@api_view(['GET'])
@permission_classes([AllowAny])
def public_teams_list(request: Request) -> Response:
    """
    Public endpoint to list all teams for signup purposes.
    No authentication required.
    """
    
    teams = Team.objects.filter(is_active=True)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
    """
    serializer_class = UserUpdateSerializer
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
