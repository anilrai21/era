from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, EmailField

from apps.core.forms import ClassInputForm


class RegisterForm(ClassInputForm, UserCreationForm):
    first_name = CharField(max_length=30, required=False, help_text="Optional.")
    last_name = CharField(max_length=30, required=False, help_text="Optional.")
    email = EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'input'


class KipaAuthenticationForm(ClassInputForm, AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
