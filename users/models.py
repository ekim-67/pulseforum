from django.db import models
from django.contrib.auth.models import User
from blog.models import Club

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #CASCADE - if user is deleted, then also delete profile
    image = models.ImageField(default='profile_pics/default_book.jpg', upload_to='profile_pics')
    bio = models.TextField(default="There isn't much here...", blank=True)
    favorite_book = models.TextField(blank=True)
    club = models.ManyToManyField(Club)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):   
        super(Profile, self).save(*args, **kwargs)  
        if not self.club.all(): 
            general = Club.objects.get_or_create(name='General')[0]
            self.club.add(general)
        
