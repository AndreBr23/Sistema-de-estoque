from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Usuario
from .serializers import CadastroUsuarioSerializer, PermissaoOperadorSerializer, UsuarioMeSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioMeSerializer(request.user)
        return Response(serializer.data)


class CadastroUsuarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CadastroUsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        return Response(UsuarioMeSerializer(usuario).data, status=status.HTTP_201_CREATED)


class OperadoresView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.perfil != Usuario.Perfil.ADMIN:
            return Response({"detail": "Apenas administradores."}, status=status.HTTP_403_FORBIDDEN)
        operadores = Usuario.objects.filter(perfil=Usuario.Perfil.OPERADOR).order_by("nome")
        return Response(PermissaoOperadorSerializer(operadores, many=True).data)


class OperadorPermissoesView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if request.user.perfil != Usuario.Perfil.ADMIN:
            return Response({"detail": "Apenas administradores."}, status=status.HTTP_403_FORBIDDEN)
        try:
            operador = Usuario.objects.get(pk=pk, perfil=Usuario.Perfil.OPERADOR)
        except Usuario.DoesNotExist:
            return Response({"detail": "Operador não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PermissaoOperadorSerializer(operador, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
