import django.forms

from catalog.models import AnswerOption, MultipleResponse, OnlyResponse, Survey


class SurveyForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    is_published = django.forms.TypedChoiceField(
        label="Публичный?",
        coerce=lambda x: x == "True",
        choices=((True, "Да"), (False, "Нет")),
    )
    is_anonymous = django.forms.TypedChoiceField(
        label="Анонимный?",
        coerce=lambda x: x == "True",
        choices=((True, "Да"), (False, "Нет")),
    )

    class Meta:
        model = Survey
        fields = (
            Survey.name.field.name,
            Survey.is_published.field.name,
            Survey.is_anonymous.field.name,
        )

        labels = {
            Survey.name.field.name: "Название",
        }

        widgets = {
            Survey.name.field.name: django.forms.TextInput(),
        }


class OnlyResponseForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    is_free = django.forms.TypedChoiceField(
        label="Свободный вопрос",
        coerce=lambda x: x == "True",
        choices=((True, "Нет"), (False, "Да")),
    )

    answer = django.forms.CharField(
        label="Правильный ответ",
        required=False,
        widget=django.forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = OnlyResponse
        fields = (
            OnlyResponse.question.field.name,
            OnlyResponse.is_free.field.name,
            OnlyResponse.answer.field.name,
        )

        labels = {
            OnlyResponse.question.field.name: "Вопрос",
            OnlyResponse.is_free.field.name: "Свободный вопрос",
        }

        widgets = {
            OnlyResponse.question.field.name: django.forms.TextInput(),
        }


class MultiResponseForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    is_free = django.forms.TypedChoiceField(
        label="Свободный вопрос",
        coerce=lambda x: x == "True",
        choices=((True, "Нет"), (False, "Да")),
    )

    answer = django.forms.CharField(
        label="Правильный ответ",
        required=False,
        widget=django.forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = OnlyResponse
        fields = (
            OnlyResponse.question.field.name,
            OnlyResponse.is_free.field.name,
            OnlyResponse.answer.field.name,
        )

        labels = {
            OnlyResponse.question.field.name: "Вопрос",
            OnlyResponse.is_free.field.name: "Свободный вопрос",
        }

        widgets = {
            OnlyResponse.question.field.name: django.forms.TextInput(),
        }


class AnswerOptionForm(django.forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = ["answer", "is_right"]


MultipleResponseFormSet = django.forms.inlineformset_factory(
    Survey,
    MultipleResponse,
    form=MultiResponseForm,
    extra=3,
    can_delete=True,
)

AnswerOptionFormSet = django.forms.inlineformset_factory(
    MultipleResponse,
    AnswerOption,
    form=AnswerOptionForm,
    extra=2,
    can_delete=True,
)


class SurveySlugForm(django.forms.Form):
    slug = django.forms.CharField(
        label="Код",
        widget=django.forms.TextInput(
            attrs={
                "class": "form-control",
            },
        ),
    )
