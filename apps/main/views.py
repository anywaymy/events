from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import Events


class MainView(ListView):
    model = Events
    template_name = "main/index.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.all()
