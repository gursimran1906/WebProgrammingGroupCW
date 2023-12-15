from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.widgets import SelectDateWidget
from datetime import datetime
from django.forms.widgets import PasswordInput

class PlaceholderTextInput(forms.TextInput):
    def __init__(self, placeholder, *args, **kwargs):
        super(PlaceholderTextInput, self).__init__(*args, **kwargs)
        self.attrs['placeholder'] = placeholder

class PlaceholderPasswordInput(forms.PasswordInput):
    def __init__(self, placeholder, render_value=False, *args, **kwargs):
        super(PlaceholderPasswordInput, self).__init__(render_value=False, *args, **kwargs)
        self.attrs['placeholder'] = placeholder


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=PlaceholderTextInput(attrs={'class': 'form-control'}, placeholder='First Name'))
    last_name = forms.CharField(max_length=30, required=True, widget=PlaceholderTextInput(attrs={'class': 'form-control'}, placeholder='Last Name'))
    username = forms.CharField(widget=PlaceholderTextInput(attrs={'class': 'form-control'}, placeholder='Username'))
    email = forms.EmailField(max_length=254, required=True, widget=PlaceholderTextInput(attrs={'class': 'form-control'}, placeholder='Email'))
    password1 = forms.CharField(widget=PlaceholderPasswordInput(attrs={'class': 'form-control'}, render_value=True, placeholder='Password'))
    password2 = forms.CharField(widget=PlaceholderPasswordInput(attrs={'class': 'form-control'}, render_value=True, placeholder='Confirm Password'))
    date_of_birth = forms.DateField(
        widget=SelectDateWidget(years=range(datetime.now().year - 100, datetime.now().year)),
        required=False,
        help_text='Optional. Enter your date of birth.'
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name','email', 'profile_image',  'date_of_birth']