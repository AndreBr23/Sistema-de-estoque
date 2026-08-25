from django.db import transaction
from rest_framework import serializers

from estoque.models import Produto
from .models import Movimentacao


class MovimentacaoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source="produto.nome", read_only=True)
    responsavel_nome = serializers.CharField(source="responsavel.nome", read_only=True)
    criado_por_nome = serializers.CharField(source="criado_por.nome", read_only=True)

    class Meta:
        model = Movimentacao
        fields = [
            "id", "produto", "produto_nome", "responsavel", "responsavel_nome", "tipo",
            "quantidade", "local_origem", "local_destino", "observacao", "criado_em", "criado_por_nome",
        ]
        read_only_fields = ["id", "criado_em", "produto_nome", "responsavel_nome", "criado_por_nome"]

    def validate(self, attrs):
        produto = attrs["produto"]
        if attrs["tipo"] == Movimentacao.Tipo.SAIDA and attrs["quantidade"] > produto.quantidade:
            raise serializers.ValidationError({"quantidade": "A saída não pode superar o estoque disponível."})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        produto = Produto.objects.select_for_update().get(pk=validated_data["produto"].pk)
        quantidade = validated_data["quantidade"]
        if validated_data["tipo"] == Movimentacao.Tipo.ENTRADA:
            produto.quantidade += quantidade
        else:
            if quantidade > produto.quantidade:
                raise serializers.ValidationError({"quantidade": "Estoque insuficiente."})
            produto.quantidade -= quantidade
        produto.save(update_fields=["quantidade", "atualizado_em"])
        return Movimentacao.objects.create(**validated_data)
