from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    language_preference = models.CharField(max_length=50, default='English')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username

class LocalGuide(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='guide_profile')
    languages = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200, blank=True)
    region = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone = models.CharField(max_length=20, blank=True)
    guide_photo = models.ImageField(upload_to='guides/', blank=True, null=True)
    references = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Guide"

    def update_rating(self):
        from reviews.models import GuideReview
        reviews = GuideReview.objects.filter(guide=self)
        if reviews.exists():
            avg = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.rating = round(avg, 1)
            self.save()
