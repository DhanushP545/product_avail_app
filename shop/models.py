from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator



class ProductCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.id} - {self.name}"
    
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Shop(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20,
        validators=[
            RegexValidator(
                regex=r'^(\+91[\-\s]?|0)?[6-9]\d{9}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],null=True)
    is_featured = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


