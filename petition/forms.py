from django import forms

from .models import Petition, Image


class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'category', 'description', 'city', 'goal']


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='Image',
        widget=forms.ClearableFileInput(attrs={'multiple':True}),
    )

    class Meta:
        model = Image
        fields = ('image',)

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
