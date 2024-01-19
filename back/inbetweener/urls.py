from django.urls import path
from .views import analyze_image

urlpatterns = [
    path('api/analyze/', analyze_image, name='analyze_image'),
]
