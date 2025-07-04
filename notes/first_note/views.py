from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .form import UserRegistrationForm, NotesForm, CommentForm, searchForm
from .models import notes
from django.db.models import Q
from .utils import extract_text_from_pdf, summarize_text, answer_question_from_text


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
    all_notes = notes.objects.all()
    comment_forms = {note.id: CommentForm() for note in all_notes}
    search_form = searchForm()
    return render(request, 'notes/notes_page.html', {'notes': all_notes, 'comment_forms': comment_forms, 'form': search_form})

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

@login_required
def comment_on_note(request, note_id):
    note = get_object_or_404(notes, id=note_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, note=note)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('comment_on_note', note_id=note.id)
    else:
        form = CommentForm(note=note)
    return render(request, 'notes/comment_on_note.html', {'note': note, 'form': form})

def search_notes(request):
    query = request.GET.get('query', '')
    if query:
        results = notes.objects.filter(Q(content__icontains=query) | Q(user__username__icontains=query))
    else:
        results = notes.objects.none()
    return render(request, 'notes/search_results.html', {'results': results, 'query': query})

@login_required
def summarize_note_pdf(request, note_id):
    note = get_object_or_404(notes, id=note_id, user=request.user)
    pdf_path = note.pdf.path  # ✅ this is the correct file path on your system
    text = extract_text_from_pdf(pdf_path)  # ✅ send path to your utils
    summary = summarize_text(text)

    return render(request, 'notes/note_summary.html', {
        'note': note,
        'summary': summary
    })

@login_required
def ask_pdf_question(request, note_id):
    note = get_object_or_404(notes, id=note_id, user=request.user)
    answer = ""
    if not note.pdf:
        return render(request, "notes/error.html", {"message": "No PDF uploaded for this note."})
    if request.method == "POST":
        question = request.POST.get("question")
        if question:
            pdf_path = note.pdf.path
            text = extract_text_from_pdf(pdf_path)
            if text:
                answer = answer_question_from_text(text, question)
            else:
                answer = "Could not extract text from the PDF."
        else:
            answer = "Please enter a question."
    return render(request, "notes/note_qa.html", {"note": note, "answer": answer})

@login_required
def add_to_favourites(request, note_id):
    note = get_object_or_404(notes, id=note_id)
    note.favourites.add(request.user)
    return redirect('notes_page')

@login_required
def remove_from_favourites(request, note_id):
    note = get_object_or_404(notes, id=note_id)
    note.favourites.remove(request.user)
    return redirect('notes_page')

@login_required
def favourite_notes(request):
    fav_notes = request.user.favourite_notes.all()
    return render(request, 'notes/favourite_notes.html', {'notes': fav_notes})

from django.shortcuts import render, get_object_or_404
from .models import notes

def branch_semesters(request, branch):
    semesters = range(1, 9)
    branch_display = dict(notes.BRANCH_CHOICES).get(branch, branch)
    return render(request, 'notes/semesters_list.html', {
        'branch': branch,
        'branch_display': branch_display,
        'semesters': semesters
    })

def notes_by_branch_semester(request, branch, semester):
    branch_display = dict(notes.BRANCH_CHOICES).get(branch, branch)
    notes_list = notes.objects.filter(branch=branch, semester=semester)
    return render(request, 'notes/notes_by_branch_semester.html', {
        'branch': branch,
        'branch_display': branch_display,
        'semester': semester,
        'notes': notes_list
    })
