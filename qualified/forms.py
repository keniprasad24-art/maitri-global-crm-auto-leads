from django import forms
from .models import Qualified

class QualifiedForm(forms.ModelForm):
    class Meta:
        model = Qualified
        fields = '__all__'
        exclude = ['status', 'created_at'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'decision_maker':
                self.fields[field].widget.attrs.update({'class': 'form-control mb-2'})