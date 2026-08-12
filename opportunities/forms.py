from django import forms
from .models import Opportunity


LOST_REASON_CHOICES = [
    ("Price Too High", "Price Too High"),
    ("Customer Not Interested", "Customer Not Interested"),
    ("Competitor Chosen", "Competitor Chosen"),
    ("No Budget", "No Budget"),
    ("No Response", "No Response"),
    ("Product Not Suitable", "Product Not Suitable"),
    ("Delayed Decision", "Delayed Decision"),
    ("Duplicate Lead", "Duplicate Lead"),
    ("Other", "Other"),
]


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "lost_reason" in self.fields:
            self.fields["lost_reason"].choices = [("", "Select Reason")] + LOST_REASON_CHOICES
