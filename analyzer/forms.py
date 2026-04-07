from django import forms
from .models import CVAnalysis


class CVAnalysisForm(forms.ModelForm):
    class Meta:
        model = CVAnalysis
        fields = ("resume", )
        widgets = {
            'resume': forms.FileInput(attrs={'class': 'form-control'})
        }