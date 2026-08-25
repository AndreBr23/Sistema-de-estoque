from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Movimentacao
from .serializers import MovimentacaoSerializer


class MovimentacaoListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MovimentacaoSerializer

    def get_queryset(self):
        queryset = Movimentacao.objects.select_related("produto", "responsavel", "criado_por")
        tipo = self.request.query_params.get("tipo")
        if self.request.user.perfil != "ADMIN":
            queryset = queryset.filter(criado_por=self.request.user)
        return queryset.filter(tipo=tipo) if tipo else queryset

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
