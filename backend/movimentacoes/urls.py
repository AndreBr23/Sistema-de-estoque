from django.urls import path
from .views import MovimentacaoListCreateView

urlpatterns = [path("", MovimentacaoListCreateView.as_view(), name="movimentacoes")]
