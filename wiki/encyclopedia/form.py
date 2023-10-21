from django import forms
from . import util

class InputForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'size':120}))
    body= forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))


class ModifyForm(forms.Form):
        title = forms.CharField(widget=forms.TextInput(attrs={'size':120}) )
        body= forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
         
    