from django.urls import path

from homepage import views

app_name = "homepage"
urlpatterns = [
    path("", views.homepage_main, name="homepage_main"),
    path("auth/", views.auth_user, name="auth_user"),
    path("register/", views.register_user, name="register_user"),
]
