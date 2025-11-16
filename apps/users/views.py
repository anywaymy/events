from django.contrib.auth.forms import SetPasswordForm
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView, View, DetailView
from django.core.mail import send_mail
from django.conf import settings


from .models import User, PasswordResetToken, UserMessage
from .forms import (UserLoginForm, UserRegistrationForm,
                    UserPasswordResetForm, StyledSetPasswordForm)

# Аутентификация и логин пользователя
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("main:index")


# Регистрация пользователя
class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        response = super().form_valid(form)

        # Создать успешное сообщение можно и таким образом (реализовано в signals)
#         msg = '<div class="modal__item">Ваш аккаунт успешно создан</div>'
#         user = form.instance
#         UserMessage.objects.create(user=user, message=msg)
        messages.success(self.request, f"Вы успешно зарегистрировались")

        return response


# View для восстановления пароля
class UserPasswordResetView(FormView):
    form_class = UserPasswordResetForm
    template_name = "users/password_reset_form.html"
    success_url = reverse_lazy("main:index")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            token_obj = PasswordResetToken.objects.create(user=user)
            reset_link = self.request.build_absolute_uri(
                reverse("users:password-confirm", args=[str(token_obj.code)])
            )

            send_mail(
                subject="Восстановление пароля",
                message="Для восстановления пароля, перейдите по данной ссылке - {} :".format(reset_link),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )

        return super().form_valid(form)


# View для сброса пароля
class UserPasswordResetConfirmView(View):
    def get(self, request, code):
        token_obj = get_object_or_404(PasswordResetToken, code=code)
        if not token_obj.is_valid():
            raise Http404("Токен недействителен")
        form = StyledSetPasswordForm(user=token_obj.user)

        return render(request, template_name="users/password_reset_confirm.html", context={"form": form})

    def post(self, request, code):
        token_obj = get_object_or_404(PasswordResetToken, code=code)
        if not token_obj.is_valid():
            raise Http404("Токен недействителен")
        form = StyledSetPasswordForm(user=token_obj.user, data=request.POST)

        if form.is_valid():
            form.save()
            token_obj.delete()
            return redirect("users:password_reset_complete")


# View для профиля пользователя
class UserProfileView(TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['message_status'] = UserMessage.objects.filter(user=self.request.user, is_read=False)

        return context


# Получение сообщений пользователя
def get_messages_from_db(request):
    user = User.objects.filter(username=request.user.username).first()
    post_data = []

    if request.method == "GET":
        for message in user.user_messages.all():

            if not message.is_read:
                message.is_read = True
                message.save()

            post_data.append({
                "id": message.id,
                "message": message.message,
                "is_read": message.is_read,
                "created_at": message.created_at.isoformat(),
            })

    return JsonResponse({'messages': post_data})


# Возвращает страницу успеха в случае успешного восстановления пароля
def password_reset_complete(request):
    return render(request, template_name="users/password_reset_complete.html")


# Logout выход из системы
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))
