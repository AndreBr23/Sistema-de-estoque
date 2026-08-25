from rest_framework import serializers

from .models import Responsavel


class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = ["id", "nome", "email", "telefone", "funcao", "ativo", "criado_em"]
        read_only_fields = ["id", "criado_em"]
