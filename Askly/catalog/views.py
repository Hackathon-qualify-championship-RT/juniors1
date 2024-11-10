import base64
from io import BytesIO

import django.db.models
from django.http import HttpResponse
import django.shortcuts
import django.utils
import matplotlib.pyplot as plt

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


def create_response_chart(survey_id):
    survey = catalog.models.Survey.objects.get(id=survey_id)

    only_responses = catalog.models.OnlyResponse.objects.filter(survey=survey)
    multiple_responses = catalog.models.MultipleResponse.objects.filter(
        survey=survey,
    )

    only_response_counts = [
        catalog.models.Answer.objects.filter(
            survey_id=survey_id,
            text__contains=response.question,
        ).count()
        for response in only_responses
    ]

    multiple_response_counts = [
        catalog.models.AnswerOption.objects.filter(response=response).count()
        for response in multiple_responses
    ]

    if sum(only_response_counts) == 0 and sum(multiple_response_counts) == 0:
        return None

    answers = catalog.models.Answer.objects.filter(survey=survey)
    answer_text = "".join([answer.text for answer in answers])

    questions = ["Верные ответы", "Неверные ответы"]
    response_counts = [answer_text.count("+"), answer_text.count("-")]

    if not any(response_counts):
        return None

    try:
        fig, ax = plt.subplots()
        ax.pie(
            response_counts,
            labels=questions,
            autopct="%1.1f%%",
            startangle=90,
        )
        ax.axis("equal")

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png).decode("utf-8")
        return graphic
    except ValueError:
        return None


def survey_detail(request, pk):
    template_name = "catalog/survey_detail.html"
    user = request.user
    survey = django.shortcuts.get_object_or_404(
        catalog.models.Survey.objects,
        user_id=user.id,
        pk=pk,
    )
    form = catalog.forms.SurveyForm(request.POST or None, instance=survey)

    if form.is_valid() and request.method == "POST":
        form.save()
        return django.shortcuts.redirect("catalog:survey_list")

    only_responses = catalog.models.OnlyResponse.objects.filter(
        survey_id=survey.id,
    )
    multiple_response = catalog.models.MultipleResponse.objects.filter(
        survey_id=survey.id,
    )

    graphic = create_response_chart(pk)

    content = {
        "form": form,
        "survey": survey,
        "only_responses": only_responses,
        "multiple_response": multiple_response,
        "graphic": graphic,
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
        return django.shortcuts.redirect("catalog:survey_detail", pk=survey.pk)

    content = {
        "form": form,
    }
    return django.shortcuts.render(request, template_name, content)


def survey_response_new_multi(request, survey_id):
    template_name = "catalog/response_create_multi.html"
    user = request.user

    if request.method == "POST":
        question_text = request.POST.get("question")
        answers = request.POST.getlist("answers")
        is_right_flags = request.POST.getlist("is_right")
        is_free = request.POST.get("is_free")

        survey = django.shortcuts.get_object_or_404(
            catalog.models.Survey.objects,
            user_id=user.id,
            pk=survey_id,
        )

        response = catalog.forms.MultipleResponse.objects.create(
            question=question_text,
            is_free=is_free,
        )

        response.survey = survey
        response.save()

        for idx, answer_text in enumerate(answers):
            is_right = (idx < len(is_right_flags)
                        and is_right_flags[idx] == "on")
            catalog.forms.AnswerOption.objects.create(
                response=response,
                answer=answer_text,
                is_right=is_right,
            )

        return django.shortcuts.redirect("catalog:survey_detail", pk=survey.pk)

    return django.shortcuts.render(request, template_name)


def survey_answer_open(request):
    template_name = "catalog/survey_answer_open.html"
    form = catalog.forms.SurveySlugForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        slug = form.cleaned_data["slug"]
        return django.shortcuts.redirect(
            "catalog:survey_answer_form",
            slug=slug,
        )

    content = {
        "form": form,
    }

    return django.shortcuts.render(request, template_name, content)


def survey_answer_form(request, slug):
    template_name = "catalog/survey_answer_form.html"

    try:
        survey = catalog.models.Survey.objects.get(
            slug=slug,
            is_published=True,
        )
    except catalog.models.Survey.DoesNotExist:
        content = {"text": "Не найден опрос :("}
        return django.shortcuts.render(
            request,
            "catalog/response_answer_ok.html",
            content,
        )

    only_response = catalog.models.OnlyResponse.objects.filter(
        survey_id=survey.id,
    )

    multi_response = catalog.models.MultipleResponse.objects.filter(
        survey_id=survey.id,
    )

    answer = catalog.models.Answer()
    if request.method == "POST":
        if not survey.is_anonymous:
            answer.name = request.POST.get("user_name")

        answer_text = "Открытые вопросы\n"
        for response in only_response:
            user_answer = request.POST.get(f"only_response_{response.id}")
            answer_text += response.question + ": " + user_answer
            if response.is_free:
                if response.answer.lower() == user_answer.lower():
                    answer_text += " +"
                else:
                    answer_text += " -"

            answer_text += "\n"

        answer_text += "\nЗакрытые вопросы\n"
        for response in multi_response:
            options = catalog.models.AnswerOption.objects.filter(
                response_id=response.id,
            )
            answer_text += response.question + "\n"
            for option in options:
                option_text = request.POST.get(
                    f"multi_response_{response.id}_{option.id}",
                )

                if option_text:
                    answer_text += f"{option.answer}: выбран"
                else:
                    answer_text += f"{option.answer}: не выбран"

                if not response.is_free:
                    if option_text and bool(option_text) != option.is_right:
                        answer_text += " +"
                    elif option_text:
                        answer_text += " -"

                answer_text += "\n"

            answer_text += "\n"

        answer.text = answer_text
        answer.survey = survey
        answer.save()
        content = {"text": "Спасибо за пройденный опрос!"}

        return django.shortcuts.render(
            request,
            "catalog/response_answer_ok.html",
            content,
        )

    content = {
        "title": survey.name,
        "is_anonymous": survey.is_anonymous,
        "only_response": only_response,
        "multi_response": multi_response,
    }

    return django.shortcuts.render(request, template_name, content)


def survey_download(request, survey_id):
    answers = catalog.models.Answer.objects.filter(
        survey_id=survey_id,
    )

    text_answer = ""

    for answer in answers:
        answer_name = ""
        if answer.name:
            answer_name = f"{answer.name}: "

        text_answer += f"{answer_name}{answer.text}\n\n"

    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = 'attachment; filename="results.txt"'

    response.write(text_answer)

    return response


def survey_del(request, survey_id):
    user = request.user
    try:
        survey = catalog.models.Survey.objects.get(
            user=user.id,
            id=survey_id,
        )
    except catalog.models.Survey.DoesNotExist:
        return django.shortcuts.redirect("catalog:survey_list")

    survey.delete()

    return django.shortcuts.redirect("catalog:survey_list")
