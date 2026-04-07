from django.urls import path
from .views import UploadView, ResultView
urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload'),
    path('result/', ResultView.as_view(), name='result'),
]
