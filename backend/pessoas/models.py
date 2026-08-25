from django.conf import settings
from django.db import models


class Responsavel(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    funcao = models.CharField(max_length=120)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="responsaveis_criados"
    )

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} — {self.funcao}"
