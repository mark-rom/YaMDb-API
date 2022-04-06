from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from reviews.models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации унаследованная от дефолтной"""
    class Meta:
        model = User
        fields = ('username', 'email', 'confirmation_code')


class CustomUserChangeForm(UserChangeForm):
    """Форма изменения пароля унаследованная от дефолтной"""
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields
