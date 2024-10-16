from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager 
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, SmartResize

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Review(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)
    review_of_the_week = models.BooleanField(default=False)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )    
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    product_link = models.URLField(blank=True, null=True)  # Product link field
    product_code = models.CharField(max_length=100, blank=True, null=True)
    tags = TaggableManager()  # Tags field to store multiple tags
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    optimized_image = ImageSpecField(source='image',processors=[SmartResize(800, 800)],format='WEBP',options={'quality': 70})
    thumbnail = ImageSpecField(source='image',processors=[ResizeToFill(200, 200)],format='WEBP',options={'quality': 60})
    views = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['-publication_date'] 
        
    def get_absolute_url(self):
        return reverse('review_detail', args=[self.slug])  

    def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.title)
            super().save(*args, **kwargs)  # Save the object to generate the primary key

    def __str__(self):
        return self.title
