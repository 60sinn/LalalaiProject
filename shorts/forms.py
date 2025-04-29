from django import forms
from .models import Short

class ShortUploadForm(forms.ModelForm):
    class Meta:
        model = Short
        fields = ['title', 'description', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input w-full rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea w-full rounded-lg'}),
            'video': forms.FileInput(attrs={'accept': 'video/mp4,video/webm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если это редактирование (instance передан), то убираем поле video
        if self.instance and self.instance.pk:
            self.fields.pop('video')

    def clean_video(self):
        video = self.cleaned_data.get('video')

        if video and hasattr(video, 'size'):
            if video.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Файл слишком большой (максимум 10 МБ).")

        if video and hasattr(video, 'content_type'):
            allowed_types = ['video/mp4', 'video/webm']
            if video.content_type not in allowed_types:
                raise forms.ValidationError("Разрешены только видеофайлы в форматах MP4 или WEBM.")

        return video
