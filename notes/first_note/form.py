from django import forms
from .models import notes
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

class NotesForm(forms.ModelForm):
    class Meta:
        model = notes
        fields = ['content', 'pdf']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'pdf': forms.ClearableFileInput(attrs={'accept': '.pdf'}),
        }
        labels = {
            'content': 'Note Content',
            'pdf': 'Upload PDF (optional)',
        }