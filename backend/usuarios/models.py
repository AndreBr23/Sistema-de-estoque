from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Perfil(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        OPERADOR = "OPERADOR", "Operador"

    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    perfil = models.CharField(
        max_length=10,
        choices=Perfil.choices,
        default=Perfil.OPERADOR,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} - {self.perfil}"

    @property
    def is_admin_perfil(self):
        return self.perfil == self.Perfil.ADMIN
class PermissaoExtra(models.Model):
    class Codigo(models.TextChoices):
        HISTORICO_GERAL_MOVIMENTACOES = (
            "HISTORICO_GERAL_MOVIMENTACOES",
            "Ver histórico geral de movimentações",
        )
        HISTORICO_GERAL_CADASTROS = (
            "HISTORICO_GERAL_CADASTROS",
            "Ver histórico geral de cadastros",
        )
        HISTORICO_GERAL_FUNCIONARIOS = (
            "HISTORICO_GERAL_FUNCIONARIOS",
            "Ver histórico geral de funcionários",
        )
        CADASTRAR_FUNCIONARIO = (
            "CADASTRAR_FUNCIONARIO",
            "Cadastrar funcionário",
        )
        EDITAR_PRODUTO = (
            "EDITAR_PRODUTO",
            "Editar produto",
        )
        TRANSFERIR_MATERIAL = (
            "TRANSFERIR_MATERIAL",
            "Transferir material",
        )
        AJUSTAR_ESTOQUE = (
            "AJUSTAR_ESTOQUE",
            "Ajustar estoque",
        )
        GERAR_EXCEL = (
            "GERAR_EXCEL",
            "Gerar relatório Excel",
        )

    codigo = models.CharField(
        max_length=50,
        choices=Codigo.choices,
        unique=True,
    )
    usuarios = models.ManyToManyField(
        Usuario,
        related_name="permissoes_extras",
        blank=True,
    )

    def __str__(self):
        return self.get_codigo_display()
