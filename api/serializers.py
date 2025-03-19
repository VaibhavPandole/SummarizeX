from django.contrib.auth.models import User

from rest_framework import serializers

from api.models import SummaryBulletPoints


class SummaryBulletPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryBulletPoints
        fields = ["original_text", "summary", "bullet_points"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Serializer to handle user registration, including password validation
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["password", "email"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            password=validated_data["password"],
            email=validated_data["email"],
        )
        return user
