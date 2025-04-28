# relatorios/urls.py
from django.urls import path
from .views import RelatorioUsuarioView, RelatorioTesteView, LoginView

urlpatterns = [
    path('usuario/', RelatorioUsuarioView.as_view(), name='relatorio-usuario-atual'),
    path('usuario/<int:user_id>/', RelatorioUsuarioView.as_view(), name='relatorio-usuario'),
    path('login/', LoginView.as_view(), name='api-login'),
    # REMOVER DEPOIS DO TESTE:
    path('teste/', RelatorioTesteView.as_view(), name='relatorio-teste'),
    # FIM DO TRECHO A REMOVER
]