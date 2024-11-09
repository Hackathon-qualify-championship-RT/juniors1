import django.contrib.auth.forms
import django.contrib.auth.models as auth_models
import django.forms as forms


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        fields = [
            auth_models.User.email.field.name,
            auth_models.User.username.field.name,
            "password1",
            "password2",
        ]


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.birthday:
            self.initial["birthday"] = self.instance.birthday.strftime(
                "%Y-%m-%d",
            )

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class UserChangeForm(django.contrib.auth.forms.UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        fields = [
            auth_models.User.first_name.field.name,
            auth_models.User.last_name.field.name,
            auth_models.User.email.field.name,
        ]
        exclude = [
            auth_models.User.password.field.name,
        ]
