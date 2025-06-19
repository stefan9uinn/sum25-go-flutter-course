from django.urls import path

from .views import TemplateRetreiveView, TemplateListCreateView


urlpatterns = [
    path('<int:pk>/', TemplateRetreiveView.as_view()),
    path('', TemplateListCreateView.as_view()),
]