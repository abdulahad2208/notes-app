from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .form import UserRegistrationForm


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
