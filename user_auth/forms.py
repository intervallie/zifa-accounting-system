from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserAccount
class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'password1', 'password2', 'role']

class AccountChangeForm(UserChangeForm):
    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'role', 'is_active']
