

from django.db import models
from leads.models import Lead 

class InitialContact(models.Model):
    METHOD_CHOICES = [
        ('phone', 'Phone Call'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('video_call', 'Video Call'),
        ('office_visit', 'Office Visit'),
    ]
    STATUS_CHOICES = [
        ('interested', 'Interested'),
        ('follow_up', 'Follow-up'),
        ('not_interested', 'Not Interested'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    contact_date = models.DateField()
    contact_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    contact_person = models.CharField(max_length=100)
    discussion_summary = models.TextField()
    customer_response = models.TextField()
    next_followup_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='follow_up')

def __str__(self):
        return f"{self.lead.name} - {self.contact_date}"

class DiscoveryMeeting(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    meeting_date = models.DateField()
    business_challenges = models.TextField()
    existing_process = models.TextField()
    pain_points = models.TextField()
    expected_outcomes = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    decision_maker = models.CharField(max_length=200)
    timeline = models.CharField(max_length=100)
class RequirementAnalysis(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="analyses")
    analysis_date = models.DateField(auto_now_add=True)
    functional_requirements = models.TextField(verbose_name="Functional Requirements (काय हवे आहे?)")
    technical_requirements = models.TextField(verbose_name="Technical Requirements (तांत्रिक गरजा)")
    proposed_solution = models.TextField(verbose_name="Proposed Solution (आपण काय देणार आहोत?)")
    
    estimated_timeline = models.CharField(max_length=100, verbose_name="अपेक्षित कालावधी (उदा. २ महिने)")
    estimated_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    potential_risks = models.TextField(blank=True, null=True, verbose_name="Potential Risks")
    final_remarks = models.TextField(blank=True, null=True)

def __str__(self):
    return f"Analysis: {self.lead.name}"