from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


from user.models import CustomUser


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
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

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class UserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Imię',
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Nazwisko',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email',
        })
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
