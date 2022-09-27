from django.db import models
from django.conf import settings

class Cause(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    name = models.CharField(max_length=155, unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    organization = models.CharField(max_length=150, null=True)
    title = models.CharField(max_length=150)
    cause = models.ManyToManyField(Cause, related_name='events')
    description = models.TextField()
    requirements = models.TextField()
    image = models.FileField(upload_to='events', default='image.png')
    when = models.CharField(max_length=255, null=True)
    skills = models.ManyToManyField(Skill, related_name='skill_events')
    goodfor = models.ManyToManyField(Profile, related_name='profile_events')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_events', on_delete=models.CASCADE)
    city = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    volunteers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='events', blank=True)
    apply = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)


class Candidate(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    message = models.TextField(null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='candidates')

    def __str__(self):
        return self.email