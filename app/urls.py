from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('create/', views.create_note),
    path('note/<int:note_id>/', views.view_note),
    path('delete/<int:note_id>/', views.delete_note),

    path('delete-media/<int:media_id>/', views.delete_media),
]