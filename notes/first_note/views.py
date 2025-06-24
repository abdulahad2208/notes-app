from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .form import UserRegistrationForm, NotesForm
from .models import notes


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.password = form.cleaned_data['password1']
            user.save()
            login(request, user)
            return redirect('index')
            
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def notes_page(request):
    all_notes=notes.objects.all()
    return render(request, 'notes/notes_page.html', {'notes': all_notes})

@login_required
def upload_notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('notes_page')
    else:
        form = NotesForm()
    return render(request, 'notes/upload_notes.html', {'form': form})

def profile(request, username):
    user_obj = User.objects.get(username=username)
    user_notes = notes.objects.filter(user=user_obj)
    return render(request, 'notes/profile.html', {'user': user_obj, 'notes': user_notes})

@login_required
def like_note(request, note_id):
    note = get_object_or_404(notes, id=note_id)
    if request.user in note.likes.all():
        note.likes.remove(request.user)
    else:
        note.likes.add(request.user)
    return redirect('notes_page')

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(notes, id=note_id)
    if request.user == note.user:
        note.delete()
        return redirect('notes_page')
    else:
        return render(request, 'notes/error.html', {'message': 'You are not authorized to delete this note.'})
    
@login_required
def edit_note(request, note_id):
    note = get_object_or_404(notes, id=note_id)
    if request.user == note.user:
        if request.method == 'POST':
            form = NotesForm(request.POST, request.FILES, instance=note)
            if form.is_valid():
                form.save()
                return redirect('notes_page')
        else:
            form = NotesForm(instance=note)
        return render(request, 'notes/edit_note.html', {'form': form})
    else:
        return render(request, 'notes/error.html', {'message': 'You are not authorized to edit this note.'})
