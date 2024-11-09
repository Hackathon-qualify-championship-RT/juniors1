import django.contrib.auth.views as auth_views
import django.urls

import users.views

app_name = "users"

urlpatterns = [
    django.urls.path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    django.urls.path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="users/logout.html",
        ),
        name="logout",
    ),
    django.urls.path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=django.urls.reverse_lazy(
                "users:change-password-done",
            ),
        ),
        name="change-password",
    ),
    django.urls.path(
        "signup/",
        users.views.RegistrationView.as_view(),
        name="signup",
    ),
]
