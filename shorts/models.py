from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from anime.models import Anime
import string
import random
 
User = get_user_model()
 
def generate_unique_url_id():
    length = 10
    characters = string.ascii_letters + string.digits
    while True:
        url_id = ''.join(random.choices(characters, k=length))
        if not Short.objects.filter(url_id=url_id).exists():
            return url_id
 
class Short(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    video = CloudinaryField(resource_type='video')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shorts')
    anime = models.ForeignKey(Anime, on_delete=models.SET_NULL, null=True, blank=True, related_name='shorts')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_shorts', blank=True)
    url_id = models.CharField(max_length=12, unique=True, blank=True)
 
    def save(self, *args, **kwargs):
        if not self.url_id:
            self.url_id = generate_unique_url_id()
        super().save(*args, **kwargs)
 
    def __str__(self):
        return self.title