from django.db import models
from core.models.userModels import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add any other attributes specific to a product

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=255)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Add any other attributes specific to a product review

class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()
    rated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add any other attributes specific to a product rating

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add any other attributes specific to an order

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add any other attributes specific to an order item

class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    # Add any other attributes specific to order history