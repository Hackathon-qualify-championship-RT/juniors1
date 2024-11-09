import django.db.models
import django.http
import django.shortcuts
import django.utils

import catalog.forms
import catalog.models


def survey_list(request):
    user = request.user

    if not user.is_authenticated:
        return django.shortcuts.redirect("homepage:homepage_main")

    template_name = "catalog/survey_list.html"
    surveys = catalog.models.Survey.objects.filter(
        user_id=user.id,
    )
    content = {"surveys": surveys, "title": "Опросы"}
    return django.shortcuts.render(request, template_name, content)


def survey_detail(request, pk):
    template_name = "catalog/survey_detail.html"
    user = request.user
    form = catalog.forms.SurveyForm(request.POST or None)

    survey = django.shortcuts.get_object_or_404(
        catalog.models.Survey.objects,
        user_id=user.id,
        pk=pk,
    )

    if form.is_valid() and request.method == "POST":
        survey.name = form.cleaned_data["name"]
        survey.is_published = form.cleaned_data["is_published"]
        survey.is_anonymous = form.cleaned_data["is_anonymous"]
        survey.save()
        return django.shortcuts.redirect("catalog:survey_list")

    only_responses = catalog.models.OnlyResponse.objects.filter(
        survey_id=survey.id,
    )
    multiple_response = catalog.models.MultipleResponse.objects.filter(
        survey_id=survey.id,
    )

    content = {
        "form": form,
        "survey": survey,
        "only_responses": only_responses,
        "multiple_response": multiple_response,
    }
    return django.shortcuts.render(request, template_name, content)


def survey_create(request):
    template_name = "catalog/survey_create.html"
    user = request.user
    if not user.is_authenticated:
        return django.shortcuts.redirect("homepage:homepage_main")

    form = catalog.forms.SurveyForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        survey = form.save()
        survey.user = user
        survey.save()
        return django.shortcuts.redirect("catalog:survey_list")

    content = {
        "form": form,
    }
    return django.shortcuts.render(request, template_name, content)


def survey_delete_only(request, survey_id, response_id):
    user = request.user
    if not user.is_authenticated:
        return django.shortcuts.redirect("homepage:homepage_main")

    response = catalog.models.OnlyResponse.objects.filter(
        survey_id=survey_id,
        pk=response_id,
    )
    response.delete()

    return django.shortcuts.redirect(f"/catalog/{survey_id}")


def survey_delete_multi(request, survey_id, response_id):
    user = request.user
    if not user.is_authenticated:
        return django.shortcuts.redirect("homepage:homepage_main")

    response = catalog.models.MultipleResponse.objects.filter(
        survey_id=survey_id,
        pk=response_id,
    )
    response.delete()

    return django.shortcuts.redirect(f"/catalog/{survey_id}")


def survey_response_new_only(request, survey_id):
    template_name = "catalog/response_create.html"
    user = request.user
    if not user.is_authenticated:
        return django.shortcuts.redirect("homepage:homepage_main")

    form = catalog.forms.OnlyResponseForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        survey = django.shortcuts.get_object_or_404(
            catalog.models.Survey.objects,
            user_id=user.id,
            pk=survey_id,
        )
        response = form.save()
        response.survey = survey
        response.save()
        return django.shortcuts.redirect("catalog:survey_list")

    content = {
        "form": form,
    }
    return django.shortcuts.render(request, template_name, content)


def survey_response_new_multi(request, survey_id):
    template_name = 'catalog/response_create_multi.html'
    user = request.user

    if request.method == 'POST':
        question_text = request.POST.get('question')
        answers = request.POST.getlist('answers')
        is_right_flags = request.POST.getlist('is_right')
        is_free = request.POST.get("is_free")

        survey = django.shortcuts.get_object_or_404(
            catalog.models.Survey.objects,
            user_id=user.id,
            pk=survey_id,
        )

        response = catalog.forms.MultipleResponse.objects.create(
            question=question_text,
            is_free=is_free
        )

        response.survey = survey
        response.save()

        for idx, answer_text in enumerate(answers):
            is_right = idx < len(is_right_flags) and is_right_flags[
                idx] == 'on'
            catalog.forms.AnswerOption.objects.create(
                response=response,
                answer=answer_text,
                is_right=is_right
            )

        return django.shortcuts.redirect(
            'catalog:survey_list')  # Перенаправление на страницу списка опросов
    return django.shortcuts.render(request, template_name)
