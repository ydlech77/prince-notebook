from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, NoteMedia
import os


# =========================
# HOME
# =========================
def home(request):
    notes = Note.objects.all().order_by('-updated_at')
    return render(request, 'home.html', {'notes': notes})


# =========================
# CREATE NOTE
# =========================
def create_note(request):

    if request.method == "POST":

        note = Note.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            password=request.POST.get('password')
        )

        return redirect(f'/note/{note.id}/')

    return render(request, 'create.html')


# =========================
# VIEW + EDIT NOTE
# =========================
def view_note(request, note_id):

    note = get_object_or_404(Note, id=note_id)

    session_key = f'note_{note.id}_unlocked'

    # =========================
    # PASSWORD CHECK
    # =========================
    if note.password is not None and note.password != "":

        if not request.session.get(session_key):

            if request.method == "POST":

                entered_password = request.POST.get('unlock_password')

                if entered_password == note.password:
                    request.session[session_key] = True
                    return redirect(f'/note/{note.id}/')
                else:
                    return render(request, 'unlock.html', {
                        'note': note,
                        'error': 'Wrong password'
                    })

            return render(request, 'unlock.html', {'note': note})

    # =========================
    # UPDATE NOTE
    # =========================
    if request.method == "POST" and not request.POST.get('unlock_password'):

        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()

        # =========================
        # MULTIPLE MEDIA UPLOAD
        # =========================
        files = request.FILES.getlist('files')

        for f in files:

            file_type = "file"

            content_type = getattr(f, 'content_type', '')

            if content_type.startswith('image'):
                file_type = "image"

            elif content_type.startswith('video'):
                file_type = "video"

            NoteMedia.objects.create(
                note=note,
                file=f,
                media_type=file_type
            )

        return redirect(f'/note/{note.id}/')

    media = note.media.all().order_by('-created_at')

    return render(request, 'note.html', {
        'note': note,
        'media': media
    })

# =========================
# DELETE NOTE
# =========================
def delete_note(request, note_id):

    note = get_object_or_404(Note, id=note_id)

    # delete all media files first
    for m in note.media.all():

        if os.path.isfile(m.file.path):
            os.remove(m.file.path)

    note.delete()

    return redirect('/')


# =========================
# DELETE SINGLE MEDIA
# =========================
def delete_media(request, media_id):

    media = get_object_or_404(NoteMedia, id=media_id)
    note_id = media.note.id

    file_path = media.file.path

    # First delete DB record safely
    media.delete()

    # Then try deleting file
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except PermissionError:
        # file is locked (video still open, browser, etc.)
        pass

    return redirect(f'/note/{note_id}/')