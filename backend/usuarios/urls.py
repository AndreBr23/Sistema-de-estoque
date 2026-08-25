from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CadastroUsuarioView, MeView, OperadorPermissoesView, OperadoresView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("cadastro/", CadastroUsuarioView.as_view(), name="cadastro"),
    path("operadores/", OperadoresView.as_view(), name="operadores"),
    path("operadores/<int:pk>/permissoes/", OperadorPermissoesView.as_view(), name="operador-permissoes"),
]
