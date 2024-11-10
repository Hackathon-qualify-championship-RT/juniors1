import django.conf
import django.contrib.auth
import django.contrib.auth.decorators
import django.contrib.auth.forms
import django.contrib.auth.mixins
import django.contrib.auth.tokens
import django.core.mail
import django.core.signing
import django.http
import django.shortcuts
import django.template.loader
import django.urls
import django.utils.encoding
import django.utils.http
import django.views
import django.views.generic

import users.forms


class RegistrationView(django.views.View):
    template_name = "users/signup.html"

    def get(self, request):
        form = users.forms.SignUpForm()
        context = {"form": form}
        return django.shortcuts.render(request, self.template_name, context)

    def post(self, request):
        form = users.forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            django.contrib.messages.success(
                request,
                "Вы зарегистрированы. Войдите с новыми данными",
            )

            return django.shortcuts.redirect("users:login")

        context = {"form": form}
        return django.shortcuts.render(request, self.template_name, context)


class ActivateView(django.views.View):
    template_name = "users/activation_success.html"

    def get(self, request, signed_username):
        user_model = django.contrib.auth.get_user_model()
        signer = django.core.signing.TimestampSigner()

        try:
            username = signer.unsign(signed_username, max_age=3600 * 12)
            user = user_model.objects.get(username=username)
        except (django.core.signing.BadSignature, user_model.DoesNotExist):
            return django.http.HttpResponseNotFound(
                "Неверная или просроченная ссылка активации",
            )

        user.is_active = True
        user.save()

        return django.shortcuts.render(request, self.template_name)


class UserListView(django.views.generic.ListView):
    template_name = "users/user_list.html"
    context_object_name = "user_list"
    queryset = django.contrib.auth.get_user_model().objects.filter(
        is_active=True,
    )


class UserDetailView(django.views.generic.DetailView):
    template_name = "users/user_detail.html"
    context_object_name = "user"

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return users.models.Profile.objects.user_detail(pk=pk)


class ProfileView(
    django.views.View,
    django.contrib.auth.mixins.LoginRequiredMixin,
):
    template_name = "users/profile.html"

    def get(self, request):
        user = request.user
        profile_form = users.forms.ProfileUpdateForm(instance=user.profile)
        user_form = users.forms.UserChangeForm(instance=user)
        context = {
            "user_form": user_form,
            "profile_form": profile_form,
        }
        return django.shortcuts.render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        profile_form = users.forms.ProfileUpdateForm(
            request.POST or None,
            request.FILES or None,
            instance=user.profile,
        )
        user_form = users.forms.UserChangeForm(
            request.POST or None,
            instance=user,
        )
        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user_form.save()
            request.session.modified = True
            django.contrib.messages.success(request, "Настройки сохранены.")
            return django.shortcuts.redirect("users:profile")

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
        }
        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )
