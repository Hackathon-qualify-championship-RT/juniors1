import django.db.models


class User(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
    )
    password = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
    )

    def set_password(self, raw_password):
        super().set_password(raw_password)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.name[:15]


class Survey(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
    )
    user = django.db.models.ForeignKey(
        User,
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь",
        related_name="catalog_users",
    )
    is_published = django.db.models.BooleanField(
        default=False,
        verbose_name="опубликовано",
    )
    is_anonymous = django.db.models.BooleanField(
        default=False,
        verbose_name="анонимно",
    )
    slug = django.db.models.SlugField(
        verbose_name="слаг",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "опрос"
        verbose_name_plural = "опросы"

    def __str__(self):
        return self.name[:15]


class Answer(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="имя",
    )
    survey = django.db.models.ForeignKey(
        Survey,
        on_delete=django.db.models.CASCADE,
        verbose_name="опрос",
    )
    text = django.db.models.TextField(
        verbose_name="ответ",
    )

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"

    def __str__(self):
        return self.name[:15]


class OnlyResponse(django.db.models.Model):
    survey = django.db.models.ForeignKey(
        Survey,
        on_delete=django.db.models.CASCADE,
        verbose_name="опрос",
    )
    question = django.db.models.CharField(
        max_length=150,
        verbose_name="вопрос",
    )
    is_free = django.db.models.BooleanField(
        default=False,
        verbose_name="есть ответ",
    )
    answer = django.db.models.TextField(
        verbose_name="верый ответ",
    )

    class Meta:
        verbose_name = "одиночный вопросы"
        verbose_name_plural = "одиночные вопросы"

    def __str__(self):
        return self.name[:15]


class MultipleResponse(django.db.models.Model):
    survey = django.db.models.ForeignKey(
        Survey,
        on_delete=django.db.models.CASCADE,
        verbose_name="опрос",
    )
    question = django.db.models.CharField(
        max_length=150,
        verbose_name="вопрос",
    )
    is_free = django.db.models.BooleanField(
        default=False,
        verbose_name="есть ответ",
    )
    answer = django.db.models.TextField(
        verbose_name="верый ответ",
    )

    class Meta:
        verbose_name = "многовариантные вопросы"
        verbose_name_plural = "многовариантные вопросы"

    def __str__(self):
        return self.name[:15]


class AnswerOption(django.db.models.Model):
    response = django.db.models.ForeignKey(
        MultipleResponse,
        on_delete=django.db.models.CASCADE,
        verbose_name="опрос",
        related_name="catalog_responses",
    )
    is_right = django.db.models.BooleanField(
        default=False,
        verbose_name="правильный",
    )
    answer = django.db.models.TextField(
        verbose_name="верый ответ",
    )

    class Meta:
        verbose_name = "вариант ответа"
        verbose_name_plural = "варианты ответа"

    def __str__(self):
        return self.name[:15]
