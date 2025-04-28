# relatorios/tests.py (adicionar ao arquivo existente)

from django.test import TestCase
from django.contrib.auth.models import User
from avaliacao.models import Evaluation, Evaluator, Evaluated
from avaliacao.services.relatorio_service import RelatorioService
import json
from django.urls import reverse
from rest_framework.test import APIClient

class RelatorioNeonIntegrationTest(TestCase):
    def setUp(self):
        # Criar usuários de teste
        self.usuario = User.objects.create_user(username='testuser', password='12345')
        self.avaliador = User.objects.create_user(username='avaliador', password='12345')
        
        # Criar objetos de teste
        self.evaluated = Evaluated.objects.create(user=self.usuario)
        self.evaluator = Evaluator.objects.create(user=self.avaliador)
        
        # Criar avaliações de teste com as competências reais
        competencias = [
            'estagio_mudanca', 'estrutura', 'encerramento',
            'acolhimento', 'seguranca_terapeuta', 'seguranca_metodo',
            'aprofundar', 'hipoteses', 'interpretativa',
            'frase_timing', 'corpo_setting', 'insight_potencia'
        ]
        
        # Criar 3 avaliações com competências diferentes
        for i, competencia in enumerate(competencias[:3]):
            Evaluation.objects.create(
                evaluator=self.evaluator,
                evaluated=self.evaluated,
                competencia=competencia,
                nota=4.0 + (i * 0.5)  # Notas diferentes para cada competência
            )
        
        # Cliente API para testes
        self.client = APIClient()
    
    def test_servico_relatorio_com_neon(self):
        """
        Testa se o serviço de relatório consegue buscar dados do Neon
        """
        # Chamar o serviço que acessa o banco
        relatorio = RelatorioService.obter_relatorio_usuario(self.usuario.id)
        
        # Verificar se obtivemos dados do banco
        self.assertIsNotNone(relatorio)
        self.assertIn('radar_data', relatorio)
        
        # Verificar se as competências corretas foram retornadas
        self.assertEqual(len(relatorio['radar_data']), 3)
        self.assertIn('estagio_mudanca', relatorio['radar_data'])
        self.assertIn('estrutura', relatorio['radar_data'])
        self.assertIn('encerramento', relatorio['radar_data'])
    
    def test_api_post_relatorio(self):
        """
        Testa o endpoint de relatório via POST
        """
        # Autenticar o usuário
        self.client.force_authenticate(user=self.usuario)
        
        # Dados para o POST
        post_data = {
            'user_id': self.usuario.id,
            'formato': 'detalhado'  # Parâmetro adicional para teste
        }
        
        # Enviar requisição POST para o endpoint
        url = reverse('relatorio-usuario-atual')
        response = self.client.post(url, post_data, format='json')
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar os dados retornados
        self.assertIn('radar_data', response.data)
        self.assertIn('areas_foco', response.data)