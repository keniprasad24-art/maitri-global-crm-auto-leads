from django.db import models

class Qualified(models.Model):
    # Choices
    INDUSTRY_CHOICES = [
        ('technology', 'Technology'), ('manufacturing', 'Manufacturing'),
        ('healthcare', 'Healthcare'), ('finance', 'Finance'), ('other', 'Other'),
    ]
    SIZE_CHOICES = [
        ('1-10', '1-10 Employees'), ('11-50', '11-50 Employees'), ('51+', '51+ Employees'),
    ]
    TIMELINE_CHOICES = [
        ('immediate', 'Immediate'), ('1-3_months', '1-3 Months'), ('3+', '3+ Months'),
    ]

    company = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=15)
    
    # New Professional Fields
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='other')
    company_size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='1-10')
    requirement = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES, default='immediate')
    decision_maker = models.BooleanField(default=False)
    source = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(max_length=50, default="Qualified")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company