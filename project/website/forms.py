from django import forms
from .models import ContactUs
from django.utils.translation import gettext_lazy as _
from dashboard.models import *

 

class ContactForm(forms.ModelForm):
    full_name = forms.CharField(
        label=_('Full Name'),
        widget=forms.TextInput(
            attrs={
            }
        )
    )
    email = forms.EmailField(
        required=True,
        label=_('Email'),

        widget=forms.EmailInput()
    )
    mobile = forms.CharField(
        label=_('Mobile'),
        widget=forms.TextInput(
            attrs={
            }
        )
    )
    subject = forms.ModelChoiceField(
        queryset=Services.objects.all(),  # Assuming Services has relevant fields
        label=_('Subject'),
        empty_label=_("--- Select Subject ---"),  # Optional: Add a default option
        required=True
    )
   
    message = forms.CharField(
        label=_('message'),
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
            }
        ),
        required=True
    )
    class Meta:
        model = ContactUs
        fields = ['full_name' ,'mobile','email','subject','message']

