from io import BytesIO

from django.http import HttpResponse
from openpyxl import Workbook
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from movimentacoes.models import Movimentacao
from usuarios.models import Usuario


class ExportarHistoricoExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        permitido = request.user.perfil == Usuario.Perfil.ADMIN or request.user.permissoes_extras.filter(
            codigo="GERAR_EXCEL"
        ).exists()
        if not permitido:
            return HttpResponse("Sem permissão para gerar Excel.", status=403)

        planilha = Workbook()
        aba = planilha.active
        aba.title = "Histórico de movimentações"
        aba.append(["Tipo", "Produto", "Quantidade", "Responsável", "Registrado por", "Data", "Observação"])
        registros = Movimentacao.objects.select_related("produto", "responsavel", "criado_por")
        for movimento in registros:
            aba.append([
                movimento.get_tipo_display(),
                movimento.produto.nome,
                movimento.quantidade,
                movimento.responsavel.nome if movimento.responsavel else "",
                movimento.criado_por.nome,
                movimento.criado_em.strftime("%d/%m/%Y %H:%M"),
                movimento.observacao,
            ])
        for coluna in aba.columns:
            letra = coluna[0].column_letter
            aba.column_dimensions[letra].width = min(max(len(str(c.value or "")) for c in coluna) + 2, 35)
        arquivo = BytesIO()
        planilha.save(arquivo)
        resposta = HttpResponse(
            arquivo.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        resposta["Content-Disposition"] = 'attachment; filename="historico-estoque.xlsx"'
        return resposta

# Create your views here.
