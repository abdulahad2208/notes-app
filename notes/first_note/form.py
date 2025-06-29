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

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}), label='Comment')
    
    def __init__(self, *args, **kwargs):
        self.note = kwargs.pop('note', None)
        super().__init__(*args, **kwargs)
    
    def save(self, user):
        if self.note:
            comment = self.note.comments.create(user=user, content=self.cleaned_data['content'])
            return comment
        return None
    
class searchForm(forms.Form):
    query = forms.CharField(label='Search Notes', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search notes...'}))
    
    def search(self):
        query = self.cleaned_data.get('query')
        if query:
            return notes.objects.filter(content__icontains=query)
        return notes.objects.none()