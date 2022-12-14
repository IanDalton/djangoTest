from rest_framework import serializers
from .models import Libro
from django.contrib.auth.models import User


class LibroSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    genre = serializers.CharField(max_length=255)
    year = serializers.CharField(max_length=4)
    author = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        # indicamos que use todos los campos
        fields = "__all__"
        # les decimos cuales son los de solo lectura
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            'owner')


class UserSerializer(serializers.ModelSerializer):
    libros = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Libro.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'libros']
