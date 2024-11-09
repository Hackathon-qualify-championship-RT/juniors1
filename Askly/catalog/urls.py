from django.urls import path

from catalog import views

app_name = "catalog"
urlpatterns = [
    path("", views.survey_list, name="survey_list"),
    path("<int:pk>/", views.survey_detail, name="survey_detail"),
]