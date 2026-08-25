from django.urls import path
from .views import ResponsavelListCreateView

urlpatterns = [path("", ResponsavelListCreateView.as_view(), name="responsaveis")]
