from email import message
from django import forms 
from django.conf import settings
from pkg_resources import require

from account.models import User
from .models import Event, Cause, Skill, Profile, Candidate


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['organization', 'title', 'cause', 'description', 'requirements', 'when', 'goodfor', 'city', 'country', 'image', 'apply']

    cause = forms.ModelMultipleChoiceField(queryset=Cause.objects.all(), widget=forms.CheckboxSelectMultiple)
    goodfor = forms.ModelMultipleChoiceField(queryset=Profile.objects.all(), widget=forms.CheckboxSelectMultiple)


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['email', 'phone', 'message']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Candidate with given email already exists')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('+'):
            raise forms.ValidationError('Phone should start with + (country code)')
        return phone