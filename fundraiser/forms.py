from django import forms

from .models import Fundraiser, Image


class FundraiserForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ['title', 'category', 'description', 'city', 'country', 'goal', 'deadline', 'paypal_account']

    def clean_goal(self):
        goal = self.cleaned_data.get('goal')
        if goal < 20:
            raise forms.ValidationError('Goal can not be less than 20$')
        return goal


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='Image',
        widget=forms.ClearableFileInput(attrs={'multiple':True}),
    )

    class Meta:
        model = Image
        fields = ('image',)


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, required=True)
    email = forms.EmailField(help_text="Receiver's email")
    comments = forms.CharField(required=False, widget=forms.Textarea)


class FundraiserEditForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ['title','category', 'description', 'goal', 'deadline']

    def clean_goal(self):
        goal = self.cleaned_data.get('goal')
        if goal < 20:
            raise forms.ValidationError('Goal can not be less than 20$')
        return goal
