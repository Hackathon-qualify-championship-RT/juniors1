from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("auth/", include("users.urls")),
]
