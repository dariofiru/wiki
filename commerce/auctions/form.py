from django import forms
from django.core.validators import MaxValueValidator 

class BidForm(forms.Form):
  
       # bid = forms.DecimalField(widget=forms.NumberInput(attrs={'decimal_places ':2}),validator=MaxValueValidator(5))
    bid = forms.DecimalField(label="Bid")
