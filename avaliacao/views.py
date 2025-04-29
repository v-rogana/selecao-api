# avaliacao/views.py
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Evaluator, Evaluated, Evaluation
from .serializers import EvaluationCreateSerializer, EvaluationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

def index(request):
    """Página inicial simples para o backend"""
    return HttpResponse("""
    <h1>API de Avaliação Allos</h1>
    <p>Endpoints disponíveis:</p>
    <ul>
        <li><a href="/api/get-csrf-token/">/api/get-csrf-token/</a> - Obter token CSRF</li>
        <li>/api/avaliacao/ - Enviar avaliação (POST)</li>
        <li><a href="/api/avaliacoes/">/api/avaliacoes/</a> - Listar todas avaliações</li>
    </ul>
    """)

def get_csrf_token(request):
    """
    Endpoint to get a CSRF token for the frontend
    """
    token = get_token(request)
    return JsonResponse({'csrf_token': token})

@api_view(['POST'])
@permission_classes([AllowAny])  # Remove a exigência de autenticação momentaneamente
def process_evaluation(request):
    """
    Endpoint to process evaluation form submissions
    """
    # Criar uma cópia dos dados para manipulação
    data = request.data.copy()
    
    # Converter string 'True'/'False' para boolean
    if 'is_associate' in data:
        if isinstance(data['is_associate'], str):
            data['is_associate'] = data['is_associate'].lower() == 'true'
    
    # Processar campos numéricos
    int_fields = [
        'estagio_mudanca', 'estrutura', 'encerramento',
        'acolhimento', 'seguranca_terapeuta', 'seguranca_metodo',
        'aprofundar', 'hipoteses', 'interpretativa',
        'frase_timing', 'corpo_setting', 'insight_potencia'
    ]
    
    for field in int_fields:
        if field in data:
            try:
                data[field] = int(data[field])
            except (ValueError, TypeError):
                return Response(
                    {
                        'status': 'error',
                        'errors': {field: ['Este campo deve ser um número inteiro.']}
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
    
    # Para debug - verificar os dados recebidos
    print("Dados recebidos:", data)
    
    # Verificar se temos os campos necessários
    required_fields = ['evaluator', 'evaluated', 'is_associate'] + int_fields
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return Response(
            {
                'status': 'error',
                'errors': {
                    'missing_fields': [f'Campos obrigatórios ausentes: {", ".join(missing_fields)}']
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = EvaluationCreateSerializer(data=data)
    
    if serializer.is_valid():
        evaluation = serializer.save()
        return Response(
            {
                'status': 'success',
                'id': evaluation.id,
                'message': 'Evaluation created successfully'
            }, 
            status=status.HTTP_201_CREATED
        )
    
    # Para debug - mostrar erros de validação
    print("Erros de validação:", serializer.errors)
    
    return Response(
        {
            'status': 'error',
            'errors': serializer.errors
        }, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
def get_evaluations(request):
    """
    Endpoint to get all evaluations
    """
    evaluations = Evaluation.objects.all()
    serializer = EvaluationSerializer(evaluations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_evaluation(request, pk):
    """
    Endpoint to get a specific evaluation
    """
    try:
        evaluation = Evaluation.objects.get(pk=pk)
        serializer = EvaluationSerializer(evaluation)
        return Response(serializer.data)
    except Evaluation.DoesNotExist:
        return Response(
            {'error': 'Evaluation not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )