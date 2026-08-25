from django.conf import settings
from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=160)
    categoria = models.CharField(max_length=100)
    local_aquisicao = models.CharField(max_length=180, default="Não informado")
    quantidade = models.PositiveIntegerField(default=0)
    estoque_minimo = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="produtos_criados"
    )

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome
