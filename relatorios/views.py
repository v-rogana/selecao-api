# relatorios/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from avaliacao.services.relatorio_service import RelatorioService
from avaliacao.services.analise_service import AnaliseService
from .serializers import RelatorioSerializer
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User  # Adicionado para buscar o primeiro usuário para teste

class LoginView(APIView):
    permission_classes = []  # Sem requisito de autenticação para login
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login bem-sucedido"})
        else:
            return Response(
                {"error": "Credenciais inválidas"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class RelatorioUsuarioView(APIView):
    """
    Endpoint para obter o relatório de um usuário
    
    GET/POST:
    Retorna o relatório completo com dados de radar, pontos fortes, pontos fracos e áreas de foco.
    
    Parâmetros (GET ou POST):
    - user_id (opcional): ID do usuário para o qual gerar o relatório.
                         Se não fornecido, usa o ID do usuário autenticado.
    - formato (opcional): 'resumido' ou 'detalhado' para diferentes níveis de detalhe
    
    Permissões:
    - Usuário comum pode acessar apenas seu próprio relatório
    - Staff pode acessar relatórios de qualquer usuário
    """
    # REMOVER DEPOIS DO TESTE: Comentei a proteção de autenticação
    # permission_classes = [IsAuthenticated]
    permission_classes = []  # Permitir acesso sem autenticação para testes
    
    def get(self, request, user_id=None):
        return self._gerar_relatorio(request, user_id)
    
    def post(self, request):
        # Obter user_id do corpo da requisição
        user_id = request.data.get('user_id', None)
        return self._gerar_relatorio(request, user_id)
    
    def _gerar_relatorio(self, request, user_id=None):
        # TESTE: Para desenvolvimento, se nenhum user_id for fornecido, usar o primeiro usuário
        if user_id is None:
            # Tente encontrar qualquer usuário no sistema
            try:
                user = User.objects.first()
                if user:
                    user_id = user.id
                    print(f"TESTE: Usando o primeiro usuário encontrado ID={user_id}")
                else:
                    return Response(
                        {"error": "Não há usuários no sistema para teste"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            except Exception as e:
                print(f"TESTE: Erro ao buscar usuário: {e}")
                return Response(
                    {"error": f"Erro ao buscar usuário: {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        # Em uma aplicação real, você verificaria permissões aqui:
        # if int(user_id) != request.user.id and not request.user.is_staff:
        #     return Response(
        #         {"error": "Você não tem permissão para acessar este relatório"}, 
        #         status=status.HTTP_403_FORBIDDEN
        #     )
        
        # Obter dados do relatório
        relatorio_data = RelatorioService.obter_relatorio_usuario(user_id)
        
        # Verificar se houve erro
        if "error" in relatorio_data:
            return Response(relatorio_data, status=status.HTTP_404_NOT_FOUND)
        
        # Adicionar áreas de foco ao relatório
        try:
            relatorio_data["areas_foco"] = AnaliseService.gerar_areas_foco(
                relatorio_data["pontos_fracos"]
            )
        except Exception as e:
            print(f"Erro ao gerar áreas de foco: {str(e)}")
            relatorio_data["areas_foco"] = []  # Usar lista vazia em caso de erro
        
        # Verificar formato (se enviado)
        formato = None
        if request.method == 'GET':
            formato = request.query_params.get('formato', 'detalhado')
        else:  # POST
            formato = request.data.get('formato', 'detalhado')
        
        # Se for resumido, remover alguns campos
        if formato == 'resumido':
            if 'avaliadores_distintos' in relatorio_data:
                del relatorio_data['avaliadores_distintos']
        
        # Serializar os dados
        serializer = RelatorioSerializer(relatorio_data)
        
        return Response(serializer.data)


# Classe de teste com dados fictícios (opcional, para desenvolvimento)
class RelatorioTesteView(APIView):
    """
    Endpoint para obter um relatório de teste (não requer autenticação)
    """
    permission_classes = []  # Sem restrição de autenticação
    
    def get(self, request):
        """
        Retorna um relatório de exemplo para testes
        """
        relatorio_exemplo = {
            "radar_data": {
                "estagio_mudanca": 4.5,
                "estrutura": 3.8,
                "encerramento": 4.2,
                "acolhimento": 4.7,
                "seguranca_terapeuta": 3.5,
                "seguranca_metodo": 4.0,
                "aprofundar": 3.9,
                "hipoteses": 4.1,
                "interpretativa": 3.7,
                "frase_timing": 4.3,
                "corpo_setting": 4.0,
                "insight_potencia": 4.6
            },
            "media_geral": 4.1,
            "pontos_fortes": [
                {"competencia": "acolhimento", "valor": 4.7, "diferenca": 0.6},
                {"competencia": "insight_potencia", "valor": 4.6, "diferenca": 0.5},
                {"competencia": "estagio_mudanca", "valor": 4.5, "diferenca": 0.4}
            ],
            "pontos_fracos": [
                {"competencia": "seguranca_terapeuta", "valor": 3.5, "diferenca": 0.6},
                {"competencia": "interpretativa", "valor": 3.7, "diferenca": 0.4},
                {"competencia": "estrutura", "valor": 3.8, "diferenca": 0.3}
            ],
            "areas_foco": [
                {
                    "area": "Construção de segurança e confiança como terapeuta", 
                    "descricao": "Trabalhe para melhorar suas habilidades em seguranca_terapeuta",
                    "competencia_relacionada": "seguranca_terapeuta"
                },
                {
                    "area": "Desenvolvimento de habilidades interpretativas", 
                    "descricao": "Trabalhe para melhorar suas habilidades em interpretativa",
                    "competencia_relacionada": "interpretativa"
                },
                {
                    "area": "Organização e estruturação das sessões terapêuticas", 
                    "descricao": "Trabalhe para melhorar suas habilidades em estrutura",
                    "competencia_relacionada": "estrutura"
                }
            ],
            "total_avaliacoes": 12,
            "avaliadores_distintos": 3
        }
        
        return Response(relatorio_exemplo)