from django.urls import path

from .views import MainView

app_name = "main"

urlpatterns = [
    path('', MainView.as_view(), name="index"),
    # path('events/<slug:slug>/', EventDetailView.as_view(), name="events"),
]

