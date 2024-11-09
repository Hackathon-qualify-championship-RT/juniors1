from django.urls import path

from homepage import views

app_name = "homepage"
urlpatterns = [
    path("", views.item_list, name="homepage_main"),
    path("auth/", views.item_list, name="auth_user"),
    path("register/", views.item_list, name="register_user"),
]