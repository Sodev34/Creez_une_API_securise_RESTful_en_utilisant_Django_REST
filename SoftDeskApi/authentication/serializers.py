from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class SignupSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        min_length=5, max_length=30, required=True, label="Utilisateur"
    )

    last_name = serializers.CharField(max_length=35, required=True, label="Nom")

    first_name = serializers.CharField(max_length=35, required=True, label="Prénom")

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
        label="Mot de passe",
    )

    class Meta:
        model = User
        fields = ("username", "last_name", "first_name", "email", "password")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(
            username=validated_data["username"],
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            email=validated_data["email"],
            password=make_password(password),
        )
        return user
