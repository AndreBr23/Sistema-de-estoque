from django.conf import settings
from rest_framework import serializers

from .models import PermissaoExtra, Usuario


class UsuarioMeSerializer(serializers.ModelSerializer):
    permissoes = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "nome",
            "email",
            "perfil",
            "permissoes",
        ]

    def get_permissoes(self, usuario):
        if usuario.perfil == Usuario.Perfil.ADMIN:
            return ["ACESSO_TOTAL"]

        return list(
            usuario.permissoes_extras.values_list("codigo", flat=True)
        )


class CadastroUsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, min_length=8)
    codigo_admin = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Usuario
        fields = ["nome", "email", "senha", "perfil", "codigo_admin"]

    def validate(self, attrs):
        if attrs.get("perfil") == Usuario.Perfil.ADMIN:
            codigo = getattr(settings, "ADMIN_CREATION_CODE", "gabinetefabio13")
            if attrs.get("codigo_admin") != codigo:
                raise serializers.ValidationError({"codigo_admin": "Código de administrador inválido."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("codigo_admin", None)
        senha = validated_data.pop("senha")
        email = validated_data["email"].lower()
        usuario = Usuario(username=email, email=email, **validated_data)
        usuario.set_password(senha)
        usuario.save()
        return usuario


class PermissaoOperadorSerializer(serializers.ModelSerializer):
    permissoes = serializers.PrimaryKeyRelatedField(
        source="permissoes_extras",
        queryset=PermissaoExtra.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Usuario
        fields = ["id", "nome", "email", "perfil", "permissoes"]
        read_only_fields = ["id", "nome", "email", "perfil"]

    def validate(self, attrs):
        if self.instance and self.instance.perfil == Usuario.Perfil.ADMIN:
            raise serializers.ValidationError("Permissões de administradores não podem ser alteradas.")
        return attrs
