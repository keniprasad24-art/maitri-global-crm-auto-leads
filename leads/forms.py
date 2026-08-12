from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'company', 'source', 'status', 'lead_pdf']
        
    def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields:
    self.fields[field].widget.attrs.update({'class': 'form-control mb-3'})