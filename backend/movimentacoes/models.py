from django.conf import settings
from django.db import models


class Movimentacao(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = "ENTRADA", "Entrada"
        SAIDA = "SAIDA", "Saída"

    produto = models.ForeignKey("estoque.Produto", on_delete=models.PROTECT, related_name="movimentacoes")
    responsavel = models.ForeignKey(
        "pessoas.Responsavel", on_delete=models.PROTECT, related_name="movimentacoes", null=True, blank=True
    )
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    quantidade = models.PositiveIntegerField()
    local_origem = models.CharField(max_length=180, default="Não informado")
    local_destino = models.CharField(max_length=180, default="Não informado")
    observacao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="movimentacoes_criadas"
    )

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.get_tipo_display()} {self.produto} ({self.quantidade})"
