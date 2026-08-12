from django.db import models

class Quotation(models.Model):
    quote_number = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30)

    def __str__(self):
        return self.quote_number

# Create your models here.
