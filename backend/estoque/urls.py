from django.urls import path
from .views import ProdutoListCreateView

urlpatterns = [path("", ProdutoListCreateView.as_view(), name="produtos")]
