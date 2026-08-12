from django import forms
from .models import InitialContact, DiscoveryMeeting

class InitialContactForm(forms.ModelForm):
    class Meta:
        model = InitialContact
        fields = "__all__"
        widgets = {
            'contact_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_followup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs.update({'class': 'form-control mb-2'})

class DiscoveryMeetingForm(forms.ModelForm):
    class Meta:
        model = DiscoveryMeeting
        fields = "__all__"
        widgets = {'meeting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})}
from .models import RequirementAnalysis

class RequirementAnalysisForm(forms.ModelForm):
    class Meta:
        model = RequirementAnalysis
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-2'})
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs.update({'class': 'form-control mb-2'})