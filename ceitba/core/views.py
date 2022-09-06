from django.shortcuts import render, HttpResponse
from core.models import Libro
from core.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    return render('templates/home.html')


class LibroLists(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, format=None):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):  # nuevo
        libros = Libro.objects.all().order_by('created_at')
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LibroDetails(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        libro = Libro.objects.filter(pk=pk).first()
        serializer = LibroSerializer(libro)
        if libro:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        libro = Libro.objects.filter(pk=pk).first()
        if libro:
            serializer = LibroSerializer(libro)
            libro.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        # vamos al libro que queremos modificar
        libro = self.get(request, pk)
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# clase para manejar múltiples instancias


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
# clase para manejar una única instancia


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
