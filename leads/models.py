from django.db import models


class Lead(models.Model):
    SOURCE_CHOICES = [
        ("website", "Website"),
        ("facebook", "Facebook Ads"),
        ("whatsapp", "WhatsApp"),
        ("instagram", "Instagram"),
        ("99acres", "99acres"),
        ("magicbricks", "Magicbricks"),
        ("housing", "Housing.com"),
        ("nobroker", "NoBroker"),
        ("phone", "Phone Call"),
        ("website", "Website"),
        ("manual", "Manual Entry"),
    ]

    STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Qualified", "Qualified"),
        ("Lost", "Lost"),
    ]

    # ===== Excel 21 columns =====
    sr_no = models.PositiveIntegerField(default=0)
    current_requirements = models.TextField(blank=True, default="")
    lead_received_date = models.DateField(null=True, blank=True)
    lead_source = models.CharField(max_length=100, blank=True, default="")
    reference_name = models.CharField(max_length=200, blank=True, default="")
    client_name = models.CharField(max_length=200, blank=True, default="")
    end_client = models.CharField(max_length=200, blank=True, default="")
    location = models.CharField(max_length=200, blank=True, default="")
    contact_person = models.CharField(max_length=200, blank=True, default="")
    designation = models.CharField(max_length=200, blank=True, default="")
    mobile_no = models.CharField(max_length=30, blank=True, default="")
    email_id = models.EmailField(blank=True, default="")
    one_time_recurring = models.CharField(max_length=100, blank=True, default="")
    project_duration = models.CharField(max_length=100, blank=True, default="")
    consultant_name = models.CharField(max_length=200, blank=True, default="")
    consultant_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    maitri_margin = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lead_stage = models.CharField(max_length=100, blank=True, default="")
    next_follow_up_date = models.DateField(null=True, blank=True)
    vendor_working_on = models.CharField(max_length=200, blank=True, default="")
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="New")

    # ===== Existing CRM fields retained for safety/compatibility =====
    name = models.CharField(max_length=100, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    company = models.CharField(max_length=100, default="Not Provided")
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default="manual")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    lead_pdf = models.FileField(upload_to="lead_pdfs/", blank=True, null=True)

    # Old fields from previous CRM migrations are retained.
    current_requirement = models.TextField(blank=True, null=True)
    follow_up_notes = models.TextField(blank=True, null=True)
    follow_up_status = models.CharField(max_length=100, blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    next_followup_date = models.DateField(blank=True, null=True)
    recurring_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.client_name or self.name or f"Lead {self.sr_no}"
