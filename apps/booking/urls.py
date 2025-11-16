from django.urls import path
from .views import EventDetailView, book_event

app_name = "booking"

urlpatterns = [
    path('detail/<slug:slug>/', EventDetailView.as_view(), name="detail"),
    path('booking/<int:event_id>/', book_event, name="book_event"),
]