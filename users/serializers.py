from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from teams.models import Team

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(
        max_length=150,
        min_length=3,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    is_staff = serializers.BooleanField(read_only=True)
    teams = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        required=False,
        queryset=Team.objects.all()
    )
    team_names = serializers.StringRelatedField(
        many=True,
        read_only=True,
        source='teams'
    )
    
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "teams",
            "team_names",
            "created_at",
        )
        read_only_fields = ("id", "created_at", "is_staff", "team_names")
    
    def create(self, validated_data: Any) -> Any:
        teams = validated_data.pop('teams', [])
        
        user = User.objects.create_user(**validated_data)
        
        if teams:
            user.teams.set(teams)
        
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
    
    def update(self, instance: Any, validated_data: Any) -> Any:
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user role (Admin only)
    """
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    is_staff = serializers.BooleanField(required=False)
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "is_staff")
        read_only_fields = ("username", "email")
    
    def update(self, instance: Any, validated_data: Any) -> Any:
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.save()
        return instance
    
    def validate_is_staff(self, value: bool) -> bool:
        """
        Prevent user from demoting themselves if they're the only admin
        """
        user = self.instance
        request_user = self.context['request'].user
        
        if user == request_user and user.is_staff and not value:
            admin_count = User.objects.filter(is_staff=True).count()
            if admin_count <= 1:
                raise serializers.ValidationError(
                    "Cannot demote yourself. You are the only admin."
                )
        
        return value

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LoginResponseSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "refresh",
            "access",
        )
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    def validate(self, attrs):  # type: ignore[no-untyped-def]
        self.token = attrs["refresh"]
        return attrs
    
    def save(self, **kwargs):  # type: ignore[no-untyped-def]
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError(
                "Invalid or expired token", code="invalid_token"
            )
        