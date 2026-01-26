from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Username already exists.")]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already exists.")]
    )
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]

    def validate(self, attrs):
        # normalize email
        attrs["email"] = attrs["email"].strip().lower()

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})

        # run Django password validators
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)


class MeReadSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="profile.phone", allow_blank=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone"]


class MeUpdateSerializer(serializers.ModelSerializer):
    # allow updating ONLY email + phone
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(source="profile.phone", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["email", "phone"]

    def validate_email(self, value):
        value = value.strip().lower()
        # prevent duplicate email (exclude current user)
        user = self.context["request"].user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})

        if "email" in validated_data:
            instance.email = validated_data["email"]
            instance.save(update_fields=["email"])

        # profile must exist (signals should create it)
        if profile_data and hasattr(instance, "profile"):
            if "phone" in profile_data:
                instance.profile.phone = profile_data["phone"]
                instance.profile.save(update_fields=["phone"])

        return instance
