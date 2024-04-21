from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm

from user.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Imię',
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Nazwisko',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Hasło',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Powtórz hasło',
        })


class CustomUserChangeForm(SetPasswordForm):
    pass