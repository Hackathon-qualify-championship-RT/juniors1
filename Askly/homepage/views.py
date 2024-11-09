import django.db.models
import django.http
import django.shortcuts
import django.utils

import catalog.models


def homepage_main(request):
    template_name = "homepage/main.html"
    items = catalog.models.Item.objects.published()
    content = {"items": items, "title": "Каталог"}
    return django.shortcuts.render(request, template_name, content)


def auth_user(request):
    template_name = "homepage/auth.html"
    content = {"title": "Авторизация"}
    return django.shortcuts.render(request, template_name, content)


def register_user(request):
    template_name = "homepage/register.html"
    content = {"title": "Регистрация"}
    return django.shortcuts.render(request, template_name, content)
