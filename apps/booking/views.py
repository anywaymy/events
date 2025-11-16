from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.db import IntegrityError

from .models import Booking

from apps.main.models import Events
from apps.users.models import User, UserMessage


class EventDetailView(DetailView):
    model = Events
    context_object_name = "event"
    template_name = "booking/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['message_status'] = UserMessage.objects.filter(user=self.request.user, is_read=False)

        return context


@csrf_exempt # отключает csrf защиту
def book_event(request, event_id):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Некорректный метод запроса'}, status=405)

    event = get_object_or_404(Events, pk=event_id)

    if event.free_places() <= 0:
        return JsonResponse({'status': 'error', 'message': 'Нет свободных мест'}, status=200)

    # Првоверяем на наличие бронирования у нашего пользователя
    if Booking.objects.filter(user=request.user, event=event).exists():
        return JsonResponse({'status': 'already_booked', 'message': 'Вы уже забронировали это мероприятие!'}, status=200)

    try:
        Booking.objects.create(user=request.user, event=event)
        return JsonResponse({"status": "success", "message": "Забронировано!"})
    except IntegrityError: # Типо тут проверяем на уникальность
        return JsonResponse({'status': 'already_booked', 'message': 'Вы уже забронировали это мероприятие!'}, status=200)
    except Exception as e:
        # Логирование ошибки или обработка других исключений
        return JsonResponse({'status': 'error', 'message': 'Произошла ошибка при бронировании.'}, status=500)
