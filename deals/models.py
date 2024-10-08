from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager  # Import TaggableManager for tags

class DealsCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Deal(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # New field
    link = models.URLField()  # Field to store the actual deal URL
    image = models.ImageField(upload_to='deals_images/', blank=True, null=True)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(DealsCategory, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()  # Field to store tags in the model

    def get_absolute_url(self):
        return reverse('deal_detail', args=[self.id])  # Updated to use the deal's ID

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the object to generate the primary key

    def __str__(self):
        return self.title
