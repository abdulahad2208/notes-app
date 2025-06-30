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
    path('notes/<int:note_id>/ask/', views.ask_pdf_question, name='note_ask'),
    path('notes/<int:note_id>/add_fav/', views.add_to_favourites, name='add_to_favourites'),
    path('notes/<int:note_id>/remove_fav/', views.remove_from_favourites, name='remove_from_favourites'),
    path('favourites/', views.favourite_notes, name='favourite_notes'),
    path('<str:branch>/semesters/', views.branch_semesters, name='branch_semesters'),
    path('<str:branch>/semester/<int:semester>/', views.notes_by_branch_semester, name='notes_by_branch_semester'),
]