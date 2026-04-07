from django.contrib import admin
from .models import CVAnalysis

@admin.register(CVAnalysis)
class CVAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'resume', 'result', 'created')
