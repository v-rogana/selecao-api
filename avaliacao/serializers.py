# avaliacao/serializers.py
from rest_framework import serializers
from .models import Evaluator, Evaluated, Evaluation

class EvaluatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluator
        fields = ['id', 'full_name']

class EvaluatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluated
        fields = ['id', 'full_name', 'is_associate']

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = [
            'id', 'evaluator', 'evaluated', 'evaluation_date',
            'estagio_mudanca', 'estrutura', 'encerramento',
            'acolhimento', 'seguranca_terapeuta', 'seguranca_metodo',
            'aprofundar', 'hipoteses', 'interpretativa',
            'frase_timing', 'corpo_setting', 'insight_potencia'
        ]
        read_only_fields = ['id', 'evaluation_date']

class EvaluationCreateSerializer(serializers.Serializer):
    evaluator = serializers.CharField(max_length=200)
    evaluated = serializers.CharField(max_length=200)
    is_associate = serializers.BooleanField()
    estagio_mudanca = serializers.IntegerField()
    estrutura = serializers.IntegerField()
    encerramento = serializers.IntegerField()
    acolhimento = serializers.IntegerField()
    seguranca_terapeuta = serializers.IntegerField()
    seguranca_metodo = serializers.IntegerField()
    aprofundar = serializers.IntegerField()
    hipoteses = serializers.IntegerField()
    interpretativa = serializers.IntegerField()
    frase_timing = serializers.IntegerField()
    corpo_setting = serializers.IntegerField()
    insight_potencia = serializers.IntegerField()
    
    def create(self, validated_data):
        # Extrair dados do avaliador e avaliado
        evaluator_name = validated_data.pop('evaluator')
        evaluated_name = validated_data.pop('evaluated')
        is_associate = validated_data.pop('is_associate')
        
        # Criar ou obter avaliador
        evaluator, _ = Evaluator.objects.get_or_create(full_name=evaluator_name)
        
        # Criar ou obter avaliado
        evaluated, _ = Evaluated.objects.get_or_create(
            full_name=evaluated_name,
            defaults={'is_associate': is_associate}
        )
        
        # Criar avaliação
        evaluation = Evaluation.objects.create(
            evaluator=evaluator,
            evaluated=evaluated,
            **validated_data
        )
        
        return evaluation