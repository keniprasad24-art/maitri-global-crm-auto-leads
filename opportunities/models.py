from django.db import models
from companies.models import Company
from contacts.models import Contact


class Opportunity(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=50)
    expected_close_date = models.DateField()

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Proposal Sent', 'Proposal Sent'),
        ('Negotiation', 'Negotiation'),
        ('Won', 'Won'),
        ('Lost', 'Lost'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    LOST_REASON_CHOICES = [
        ('Price Too High', 'Price Too High'),
        ('Customer Not Interested', 'Customer Not Interested'),
        ('Competitor Chosen', 'Competitor Chosen'),
        ('No Budget', 'No Budget'),
        ('No Response', 'No Response'),
        ('Product Not Suitable', 'Product Not Suitable'),
        ('Delayed Decision', 'Delayed Decision'),
        ('Duplicate Lead', 'Duplicate Lead'),
        ('Other', 'Other'),
    ]

    lost_reason = models.CharField(
        max_length=100,
        choices=LOST_REASON_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title