from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)

    class Meta:
        # Meta: Links this form to the User model and specifies the fields to include in the form.
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']