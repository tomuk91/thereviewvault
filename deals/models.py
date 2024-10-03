from django.db import models

class DealsCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Deal(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField()
    image = models.ImageField(upload_to='deals_images/', blank=True, null=True)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(DealsCategory, on_delete=models.CASCADE, blank=True, null=True)  # Make sure this is present
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

