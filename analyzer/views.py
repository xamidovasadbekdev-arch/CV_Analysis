from unittest import result

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView
from .forms import CVAnalysisForm
from .models import CVAnalysis
import os

# llm settings
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# pdf reading
import PyPDF2


def extract_text(resume_file):
    reader = PyPDF2.PdfReader(resume_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# # docs reading
# from docx import Document
# from io import BytesIO
#
# def extract_text(resume_file):
#     resume_file.seek(0)
#     doc = Document(BytesIO(resume_file.read()))
#     text = "\n".join([para.text for para in doc.paragraphs])
#     return text


class UploadView(LoginRequiredMixin, CreateView):
    template_name = 'analysis/upload.html'
    form_class = CVAnalysisForm
    success_url = reverse_lazy("result")

    def form_valid(self, form):
        form.instance.user = self.request.user

        # cv reading
        resume_file = form.cleaned_data['resume']
        text = extract_text(resume_file)
        prompt = f"""
        You are a professional HR manager. Analyze this resume and provide feedback on the 
        candidate's strengths, weaknesses, and suitability for a software engineering role(junior, middle, etc.). 
        Here is the resume content:
        {text}
        """
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        form.instance.result = response.choices[0].message.content

        return super().form_valid(form)


class ResultView(LoginRequiredMixin, TemplateView):
    template_name = 'analysis/result.html'
    context_object_name = 'analysis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['analysis'] = CVAnalysis.objects.filter(
            user=self.request.user
        ).order_by('-created').first()
        return context