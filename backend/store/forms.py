from django import forms
from django.contrib.auth.models import User
from .models import Customer

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CustomerPreferencesForm(forms.ModelForm):
    preferred_genres = forms.CharField(
        required=False,
        label="Preferred Genres (comma-separated)",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. action, sci-fi, mystery'})
    )

    class Meta:
        model = Customer
        fields = ['preferred_genres']

class EmailUpdateForm(forms.Form):
    email = forms.EmailField(label="Please enter your email to continue:")
