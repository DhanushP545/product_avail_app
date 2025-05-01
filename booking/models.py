from django.db import models
from shop.models import Product, ProductCategory, Shop
from django.contrib.auth.models import User

class PreBooking(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('confirmed_sold', 'Confirmed Sold'),
        ('cancelled', 'Cancelled'),], default='Pending')

    def __str__(self):
        return f"{self.product.name} - {self.quantity} (Buyer: {self.buyer.username})"

