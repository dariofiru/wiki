from django import forms
from django.core.validators import MaxValueValidator 
from multiselectfield import MultiSelectField
from .models import Category

class BidForm(forms.Form):
  
       # bid = forms.DecimalField(widget=forms.NumberInput(attrs={'decimal_places ':2}),validator=MaxValueValidator(5))
    bid = forms.DecimalField(label="Bid")


class AddForm(forms.Form):

    categories = Category.objects.all()

    addform_flag = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    product_name = forms.CharField(widget=forms.TextInput(attrs={'size':120}) )
    product_description= forms.CharField(widget=forms.Textarea(attrs={"rows":15, "cols":80}))
    product_img_url = forms.CharField(widget=forms.TextInput(attrs={'size':120}) )
    product_categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple())
    product_starting_bid = forms.DecimalField(label="Initail price")

class CommentForm(forms.Form):
    comment= forms.CharField(widget=forms.Textarea(attrs={"rows":9, "cols":40}))
    commentform_flag = forms.BooleanField(widget=forms.HiddenInput, initial=True)