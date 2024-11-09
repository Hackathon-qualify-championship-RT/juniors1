from django.urls import path

from catalog import views

app_name = "catalog"
urlpatterns = [
    path("", views.survey_list, name="survey_list"),
    path("<int:pk>/", views.survey_detail, name="survey_detail"),
    path("create/", views.survey_create, name="survey_create"),
    path("<int:survey_id>/1/<int:response_id>/", views.survey_delete_only, name="survey_delete_only"),
    path("<int:survey_id>/2/<int:response_id>/", views.survey_delete_multi, name="survey_delete_multi"),
    path("<int:survey_id>/1/new/", views.survey_response_new_only, name="survey_response_new_only"),
    path("<int:survey_id>/2/new/", views.survey_response_new_multi, name="survey_response_new_multi"),
]