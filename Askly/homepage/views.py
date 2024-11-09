import django.db.models
import django.http
import django.shortcuts
import django.utils


def homepage_main(request):
    template_name = "homepage/main.html"
    content = {"title": "Каталог"}
    return django.shortcuts.render(request, template_name, content)


def auth_user(request):
    template_name = "homepage/auth.html"
    content = {"title": "Авторизация"}
    return django.shortcuts.render(request, template_name, content)


def register_user(request):
    template_name = "homepage/register.html"
    content = {"title": "Регистрация"}
    return django.shortcuts.render(request, template_name, content)
