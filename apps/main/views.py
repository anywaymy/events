from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from .models import Events
from apps.users.models import UserMessage

# View для отображения всех мероприятий
class MainView(ListView):
    model = Events
    template_name = "main/index.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['message_status'] = UserMessage.objects.filter(user=self.request.user, is_read=False)

        return context


# class EventDetailView(DetailView):
#     model = Events
#     template_name = "main/event_detail.html"
