from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.food.price * self.quantity

    def is_payment_less(self):
        try:
            payment = Payment.objects.get(order=self)
            if payment.amount < self.total_price:
                return True
            else:
                return False
        except Payment.DoesNotExist:
            return False

class Payment(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)



