# avaliacao/services/analise_service.py
class AnaliseService:
    """
    Serviço responsável por analisar resultados e gerar insights
    """
    
    @staticmethod
    def gerar_areas_foco(pontos_fracos):
        """
        Gera recomendações de áreas para focar baseado nos pontos fracos
        """
        areas_foco = []
        
        # Mapeamento de competências para áreas de foco
        mapeamento_foco = {
            'estagio_mudanca': "Habilidades de avaliação do estágio de mudança do paciente",
            'estrutura': "Organização e estruturação das sessões terapêuticas",
            'encerramento': "Técnicas de encerramento e finalização adequada de sessões",
            'acolhimento': "Desenvolvimento de capacidade de acolhimento emocional",
            'seguranca_terapeuta': "Construção de segurança e confiança como terapeuta",
            'seguranca_metodo': "Domínio e aplicação consistente de métodos terapêuticos",
            'aprofundar': "Técnicas para aprofundar questões importantes durante a sessão",
            'hipoteses': "Formulação de hipóteses clínicas adequadas",
            'interpretativa': "Desenvolvimento de habilidades interpretativas",
            'frase_timing': "Aprimoramento de timing e formulação de frases terapêuticas",
            'corpo_setting': "Gestão de aspectos corporais e do setting terapêutico",
            'insight_potencia': "Facilitação de insights e potencialização do processo terapêutico"
        }
        
        for ponto in pontos_fracos:
            competencia = ponto["competencia"].lower()
            if competencia in mapeamento_foco:
                areas_foco.append({
                    "area": mapeamento_foco[competencia],
                    "descricao": f"Trabalhe para melhorar suas habilidades em {ponto['competencia']}",
                    "competencia_relacionada": ponto["competencia"]
                })
            else:
                # Caso genérico para competências não mapeadas
                areas_foco.append({
                    "area": f"Desenvolvimento em {ponto['competencia']}",
                    "descricao": f"Foque em aprimorar suas habilidades em {ponto['competencia']}",
                    "competencia_relacionada": ponto["competencia"]
                })
                
        return areas_foco