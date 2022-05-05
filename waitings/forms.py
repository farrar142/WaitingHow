from django import forms
from .models import Waiting

class PeopleGetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].required = True
        self.fields['adults'].required = True
        self.fields['kids'].required = True

    class Meta:
        model = Waiting
        fields = ['phone_number','adults', 'kids']