from django.db import models

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('Basic', 'Basic'),
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
    ]

    customer_name = models.CharField(max_length=100)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Expired', 'Expired'),
        ],
        default='Active'
    )

    def __str__(self):
        return self.customer_name
    payment_status = models.CharField(
    max_length=20,
    default="Pending"
)