from django.urls import path

from .views import ExportarHistoricoExcelView

urlpatterns = [path("historico/excel/", ExportarHistoricoExcelView.as_view(), name="historico-excel")]
