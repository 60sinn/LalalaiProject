from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.db.models import Avg
import random
import string

#жанр
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

#студия
class Studio(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

#аниме
class Anime(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='animes')
    studio = models.ForeignKey(Studio, on_delete=models.SET_NULL, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    poster = CloudinaryField('image', blank=True, null=True)
    url_title = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # тут гененрируется часть юрл если url_title не задан
        if not self.url_title:
            self.url_title = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        avg = self.ratings.aggregate(Avg('score'))['score__avg']
        return round(avg, 1) if avg else 0

#сезон
class Season(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='seasons')
    title = models.CharField(max_length=200)
    season_number = models.PositiveIntegerField()  # Номер сезона (1, 2, 3 и т.д.)
    release_date = models.DateField(null=True, blank=True)
    url_title = models.SlugField(blank=True)
    poster = CloudinaryField('image', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.url_title:
            self.url_title = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.anime.title} - Season {self.season_number})"
    
    @property
    def average_rating(self):
        avg = self.ratings.aggregate(Avg('score'))['score__avg']
        return round(avg, 1) if avg else 0

#эпизод
def generate_random_slug(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

from django.db import models

class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    url_title = models.SlugField(unique=True, blank=True)
    video = models.URLField("Video URL", blank=True, null=True)  # ⬅️ изменено

    def save(self, *args, **kwargs):
        if not self.url_title:
            while True:
                random_slug = generate_random_slug()
                if not Episode.objects.filter(url_title=random_slug).exists():
                    self.url_title = random_slug
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Episode {self.episode_number} - {self.title}"


class Opening(models.Model):
    anime = models.ForeignKey('Anime', on_delete=models.CASCADE, related_name='openings')
    title = models.CharField(max_length=255)
    url_title = models.SlugField(unique=True, blank=True)
    video = models.URLField("Video URL", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.url_title:
            while True:
                random_slug = generate_random_slug()
                if not Opening.objects.filter(url_title=random_slug).exists():
                    self.url_title = random_slug
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.anime.title} — {self.title}"

    def resolved_video_url(self):
        if self.video:
            return self.video.url if hasattr(self.video, 'url') else self.video
        return self.external_video_url