from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Responsavel
from .serializers import ResponsavelSerializer


class ResponsavelListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResponsavelSerializer
    queryset = Responsavel.objects.all()

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
