from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Club(models.Model):
    name = models.CharField(max_length=100)
    current_book = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=500, null=True)
    banner = models.ImageField(default='default-icon.jpg', upload_to='profile_pics')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) #pass in the actual function, not the executed function
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, default=1)
    
    #A foreign key is a column or a set of columns in a table whose values correspond to the values of the primary key in another table.
    #foreignkey -- one to many relationship
    #one user can have multiple posts, post can only have one user
    #on_delete = models.CASCADE -- if the user gets deleted, then the posts are deleted

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-date_posted']
    
class Comment(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) #pass in the actual function, not the executed function
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #A foreign key is a column or a set of columns in a table whose values correspond to the values of the primary key in another table.
    #foreignkey -- one to many relationship
    #one user can have multiple posts, post can only have one user
    #on_delete = models.CASCADE -- if the user gets deleted, then the comments are deleted

    def __str__(self):
        return self.content
    
    

