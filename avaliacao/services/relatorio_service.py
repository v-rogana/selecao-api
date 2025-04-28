# avaliacao/services/relatorio_service.py
from avaliacao.models import Evaluation, Evaluator, Evaluated
from django.db.models import Avg, Max, Min
from collections import defaultdict

class RelatorioService:
    """
    Serviço responsável por processar dados de avaliação e gerar relatórios
    """
    
    @staticmethod
    def obter_relatorio_usuario(user_id):
        """
        Obtém dados de avaliação de um usuário específico
        """
        print(f"Buscando relatório para o usuário ID={user_id}")
        
        try:
            # Verificar se o usuário existe
            try:
                from django.contrib.auth.models import User
                user = User.objects.get(id=user_id)
                print(f"Usuário encontrado: {user.username}")
            except User.DoesNotExist:
                print(f"Usuário ID={user_id} não encontrado")
                return {"error": "Usuário não encontrado"}
            
            # Buscar o avaliado relacionado a este usuário
            try:
                evaluated = Evaluated.objects.get(user=user)
                print(f"Avaliado encontrado: ID={evaluated.id}")
            except Evaluated.DoesNotExist:
                print(f"Não foi encontrado um avaliado para o usuário ID={user_id}")
                return {"error": "Usuário não está cadastrado como avaliado"}
            
            # Buscar todas as avaliações deste avaliado
            avaliacoes = Evaluation.objects.filter(evaluated=evaluated)
            
            # Log do número de avaliações encontradas
            print(f"Encontradas {avaliacoes.count()} avaliações")
            
            if not avaliacoes.exists():
                return {
                    "error": "Nenhuma avaliação encontrada para este usuário"
                }
                    
            # Agrupa as avaliações por competência
            dados_radar = defaultdict(list)
            
            # Lista de todas as competências no modelo Evaluation
            competencias = [
                'estagio_mudanca', 'estrutura', 'encerramento', 
                'acolhimento', 'seguranca_terapeuta', 'seguranca_metodo',
                'aprofundar', 'hipoteses', 'interpretativa', 
                'frase_timing', 'corpo_setting', 'insight_potencia'
            ]
            
            # Para cada avaliação, colete as notas de cada competência
            for avaliacao in avaliacoes:
                for competencia in competencias:
                    # Obtenha o valor da competência do objeto avaliação
                    valor = getattr(avaliacao, competencia)
                    dados_radar[competencia].append(valor)
            
            # Calcula a média de cada competência
            radar_data = {
                competencia: sum(notas) / len(notas) 
                for competencia, notas in dados_radar.items()
            }
            
            # Log das competências e notas
            print(f"Competências encontradas: {list(radar_data.keys())}")
            
            # Identificar pontos fortes e fracos
            pontos_fortes = []
            pontos_fracos = []
            
            media_geral = sum(radar_data.values()) / len(radar_data)
            
            for competencia, valor in radar_data.items():
                if valor >= media_geral * 1.1:  # 10% acima da média
                    pontos_fortes.append({
                        "competencia": competencia,
                        "valor": valor,
                        "diferenca": valor - media_geral
                    })
                elif valor <= media_geral * 0.9:  # 10% abaixo da média
                    pontos_fracos.append({
                        "competencia": competencia,
                        "valor": valor,
                        "diferenca": media_geral - valor
                    })
            
            # Ordenar pontos fortes e fracos pela diferença
            pontos_fortes.sort(key=lambda x: x["diferenca"], reverse=True)
            pontos_fracos.sort(key=lambda x: x["diferenca"], reverse=True)
            
            return {
                "radar_data": radar_data,
                "media_geral": media_geral,
                "pontos_fortes": pontos_fortes[:3],  # Top 3 pontos fortes
                "pontos_fracos": pontos_fracos[:3],  # Top 3 pontos fracos
                "total_avaliacoes": avaliacoes.count(),
                "avaliadores_distintos": avaliacoes.values('evaluator').distinct().count()
            }
            
        except Exception as e:
            print(f"Erro ao gerar relatório: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"error": f"Erro ao gerar relatório: {str(e)}"}