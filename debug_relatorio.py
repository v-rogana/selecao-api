# debug_relatorio.py
from django.contrib.auth.models import User
from avaliacao.models import Evaluated, Evaluator, Evaluation
from avaliacao.services.relatorio_service import RelatorioService

def debug_database():
    """Verifica os dados no banco de dados"""
    print("=== Verificando dados no banco ===")
    
    # Verificar usuários
    users = User.objects.all()
    print(f"Total de usuários: {users.count()}")
    if users.exists():
        for user in users[:5]:  # Mostrar até 5 usuários
            print(f"- User ID={user.id}, username={user.username}")
    
    # Verificar avaliados
    evaluateds = Evaluated.objects.all()
    print(f"\nTotal de avaliados: {evaluateds.count()}")
    if evaluateds.exists():
        for evaluated in evaluateds[:5]:
            print(f"- Evaluated ID={evaluated.id}, User ID={evaluated.user.id}")
    
    # Verificar avaliadores
    evaluators = Evaluator.objects.all()
    print(f"\nTotal de avaliadores: {evaluators.count()}")
    if evaluators.exists():
        for evaluator in evaluators[:5]:
            print(f"- Evaluator ID={evaluator.id}, User ID={evaluator.user.id}")
    
    # Verificar avaliações
    evaluations = Evaluation.objects.all()
    print(f"\nTotal de avaliações: {evaluations.count()}")
    if evaluations.exists():
        for evaluation in evaluations[:5]:
            print(f"- Evaluation ID={evaluation.id}, Evaluated ID={evaluation.evaluated.id}, " +
                  f"Competência={evaluation.competencia}, Nota={evaluation.nota}")

def tentar_relatorio():
    """Tenta gerar relatórios para todos os usuários"""
    print("\n=== Tentando gerar relatórios ===")
    
    users = User.objects.all()
    for user in users[:5]:  # Testar com até 5 usuários
        print(f"\nTestando relatório para User ID={user.id}, username={user.username}")
        relatorio = RelatorioService.obter_relatorio_usuario(user.id)
        
        if "error" in relatorio:
            print(f"ERRO: {relatorio['error']}")
        else:
            print("Relatório gerado com sucesso!")
            print(f"Competências no relatório: {list(relatorio['radar_data'].keys())}")
            print(f"Total de avaliações: {relatorio['total_avaliacoes']}")

if __name__ == "__main__":
    debug_database()
    tentar_relatorio()