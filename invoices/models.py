from django.db import models

class Invoice(models.Model):
    invoice_no = models.CharField(max_length=100)
    customer = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.invoice_no