import django.db.models
import django.http
import django.shortcuts
import django.utils

import catalog.models


def survey_list(request):
    template_name = "catalog/survey_list.html"
    surveys = catalog.models.Survey.objects
    content = {"surveys": surveys, "title": "Опросы"}
    return django.shortcuts.render(request, template_name, content)


def survey_detail(request, pk):
    template_name = "catalog/survey_detail.html"

    survey = django.shortcuts.get_object_or_404(
        catalog.models.Survey.objects,
        pk=pk,
    )
    content = {
        "survey": survey,
    }
    return django.shortcuts.render(request, template_name, content)
