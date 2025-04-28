# relatorios/serializers.py
from rest_framework import serializers

class RelatorioSerializer(serializers.Serializer):
    """
    Serializer para dados de relatório
    """
    radar_data = serializers.DictField(
        child=serializers.FloatField()
    )
    media_geral = serializers.FloatField()
    pontos_fortes = serializers.ListField(
        child=serializers.DictField()
    )
    pontos_fracos = serializers.ListField(
        child=serializers.DictField()
    )
    total_avaliacoes = serializers.IntegerField()
    avaliadores_distintos = serializers.IntegerField()
    areas_foco = serializers.ListField(
        child=serializers.DictField()
    )