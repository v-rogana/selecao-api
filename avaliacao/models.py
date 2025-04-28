# avaliacao/models.py
from django.db import models
from django.contrib.auth.models import User  # Importe o modelo User

class Evaluator(models.Model):
    """
    Model to store information about evaluators.
    """
    full_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = 'Evaluator'
        verbose_name_plural = 'Evaluators'

class Evaluated(models.Model):
    """
    Model to store information about evaluated individuals.
    """
    # Adicione a relação com o User do Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='evaluated')
    full_name = models.CharField(max_length=200)
    is_associate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = 'Evaluated'
        verbose_name_plural = 'Evaluated'

# O restante do seu modelo permanece o mesmo
class Evaluation(models.Model):
    """
    Model to store skill evaluations.
    """
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE, related_name='evaluations')
    evaluated = models.ForeignKey(Evaluated, on_delete=models.CASCADE, related_name='evaluations')
    evaluation_date = models.DateTimeField(auto_now_add=True)
    
    # Possible scores for each skill
    SCORE_CHOICES = [
        (-9, '-9'),
        (-3, '-3'),
        (-1, '-1'),
        (0, '0'),
        (1, '+1'),
        (3, '+3'),
        (9, '+9'),
    ]
    
    # Skill fields - keeping the original names for direct mapping with frontend
    estagio_mudanca = models.IntegerField(choices=SCORE_CHOICES)
    estrutura = models.IntegerField(choices=SCORE_CHOICES)
    encerramento = models.IntegerField(choices=SCORE_CHOICES)
    acolhimento = models.IntegerField(choices=SCORE_CHOICES)
    seguranca_terapeuta = models.IntegerField(choices=SCORE_CHOICES)
    seguranca_metodo = models.IntegerField(choices=SCORE_CHOICES)
    aprofundar = models.IntegerField(choices=SCORE_CHOICES)
    hipoteses = models.IntegerField(choices=SCORE_CHOICES)
    interpretativa = models.IntegerField(choices=SCORE_CHOICES)
    frase_timing = models.IntegerField(choices=SCORE_CHOICES)
    corpo_setting = models.IntegerField(choices=SCORE_CHOICES)
    insight_potencia = models.IntegerField(choices=SCORE_CHOICES)
    
    def __str__(self):
        return f"Evaluation of {self.evaluated} by {self.evaluator} on {self.evaluation_date.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluations'
        ordering = ['-evaluation_date']  # Most recent first