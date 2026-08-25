from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Produto
from .serializers import ProdutoSerializer


class ProdutoListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProdutoSerializer
    queryset = Produto.objects.select_related("criado_por").all()

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)

    def get_queryset(self):
        queryset = Produto.objects.select_related("criado_por").all()
        if self.request.query_params.get("historico") == "meu" and self.request.user.perfil != "ADMIN":
            return queryset.filter(criado_por=self.request.user)
        return queryset
