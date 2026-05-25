from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)

    # optional security
    password = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class NoteMedia(models.Model):

    MEDIA_TYPE = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('file', 'File'),
    )

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name="media"
    )

    file = models.FileField(upload_to='note_media/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_image(self):
        return self.media_type == "image"

    def is_video(self):
        return self.media_type == "video"

    def __str__(self):
        return f"{self.note.title} - {self.media_type}"