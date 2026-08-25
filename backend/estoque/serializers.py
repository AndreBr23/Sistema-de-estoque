from rest_framework import serializers

from .models import Produto


class ProdutoSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(source="criado_por.nome", read_only=True)
    situacao = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = [
            "id", "nome", "categoria", "local_aquisicao", "quantidade", "estoque_minimo",
            "situacao", "criado_em", "atualizado_em", "criado_por_nome",
        ]
        read_only_fields = ["id", "criado_em", "atualizado_em", "criado_por_nome", "situacao"]

    def get_situacao(self, produto):
        if produto.quantidade <= produto.estoque_minimo:
            return "BAIXO"
        return "OK"
