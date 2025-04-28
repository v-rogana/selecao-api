# avaliacao/admin.py
from django.contrib import admin
from .models import Evaluator, Evaluated, Evaluation

@admin.register(Evaluator)
class EvaluatorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created_at')
    search_fields = ('full_name',)

@admin.register(Evaluated)
class EvaluatedAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'is_associate', 'created_at')
    list_filter = ('is_associate',)
    search_fields = ('full_name',)

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('evaluated', 'evaluator', 'evaluation_date')
    list_filter = ('evaluation_date',)
    search_fields = ('evaluated__full_name', 'evaluator__full_name')
    date_hierarchy = 'evaluation_date'