from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from first_note import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('notes/', views.notes_page, name='notes_page'),
    path('upload_notes/', views.upload_notes, name='upload_notes'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('like_note/<int:note_id>/', views.like_note, name='like_note'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('comment/<int:note_id>/', views.comment_on_note, name='comment_on_note'),
    path('search/', views.search_notes, name='search_notes'),
    path('notes/<int:note_id>/summary/', views.summarize_note_pdf, name='note_summary'),
]