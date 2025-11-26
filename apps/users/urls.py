from django.urls import path

from .views import (UserLoginView, UserPasswordResetConfirmView,
                    UserPasswordResetView, UserProfileView,
                    UserRegistrationView, get_messages_from_db, logout,
                    password_reset_complete)

app_name = "users"

urlpatterns = [
    # user auth && profile
    path('login/', UserLoginView.as_view(), name="login"),
    path('registration/', UserRegistrationView.as_view(), name="registration"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('logout/', logout, name="logout"),

    # user recovery
    path('reset/', UserPasswordResetView.as_view(), name="reset"),
    path('password_confirm/<uuid:code>/', UserPasswordResetConfirmView.as_view(), name="password-confirm"),
    path('password_reset_complete/', password_reset_complete, name="password_reset_complete"),

    # получить сообщения
    path('get_messages/', get_messages_from_db, name="get_messages_from_db"),
]

