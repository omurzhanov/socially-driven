from django import forms

from .models import Post, Image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'description', 'city', 'phone']

    def clean_phone(self):
        data = self.cleaned_data
        phone = data['phone']
        
        if not phone.startswith('+996'):
            raise forms.ValidationError('Number should start with +996')
        
        if len(phone) != 13:
            raise forms.ValidationError('Invalid phone number')
        return phone


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='Image',
        widget=forms.ClearableFileInput(attrs={'multiple':True}),
    )

    class Meta:
        model = Image
        fields = ('image',)
