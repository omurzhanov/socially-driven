import math
from venv import create

from django.utils import timezone
from django.db import models
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Fundraiser(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='fundraisers', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fundraisers', on_delete=models.CASCADE)
    city = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    paypal_account = models.EmailField()
    goal = models.BigIntegerField(default=100)
    money_raised = models.BigIntegerField(default=0)
    deadline = models.DateField(null=True, blank=True)
    donators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='donated_fundraisers', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def get_percentage(self):
        percentage = (self.money_raised * 100) / self.goal
        return math.ceil(percentage)

    @property
    def get_image(self):
        return self.images.first()
    
    def published(self):
        now = timezone.now()
        
        diff= now - self.created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"
    
    def get_absolute_url(self):
        return reverse('fund-detail', kwargs={'pk':self.pk})

    class Meta:
        ordering = ('-created',)


class Image(models.Model):
    image = models.ImageField(upload_to='posts')
    fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.url

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='words', on_delete=models.CASCADE)
    fundraiser = models.ForeignKey(Fundraiser, related_name='words', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
    
    class Meta:
        ordering = ('-created',)


class Donation(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='donations', on_delete=models.CASCADE)
    fundraiser = models.ForeignKey(Fundraiser, related_name='donations', on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField(default=10)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.amount)