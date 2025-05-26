from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('travel', 'Travel'),
        ('food', 'Food'),
        ('lifestyle', 'Lifestyle'),
        ('business', 'Business'),
        ('arts', 'Arts & Culture'),
    ]

    title = models.CharField(max_length=200)
    featured_image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    excerpt = models.TextField(max_length=300)
    content = models.TextField()
    tags = models.CharField(max_length=200, help_text='Comma-separated tags')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title