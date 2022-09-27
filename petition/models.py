from django.db import models
from django.conf import settings
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Petition(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_petitions')
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='petitions')
    city = models.CharField(max_length=150)
    goal = models.PositiveIntegerField(default=100)
    created = models.DateTimeField(auto_now_add=True)
    signers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='petitions', blank=True)

    def __str__(self):
        return self.title

    @property
    def get_image(self):
        return self.images.first()
    
    @property
    def get_percentage(self):
        percentage = (self.signers.count() * 100) / self.goal
        return percentage
    
    def get_absolute_url(self):
        return reverse('petition-detail', kwargs={'pk':self.pk})
    class Meta:
        ordering = ['-created',]


class Image(models.Model):
    image = models.ImageField(upload_to='posts')
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.url


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    petition = models.ForeignKey(Petition, related_name='comments', on_delete=models.CASCADE)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
