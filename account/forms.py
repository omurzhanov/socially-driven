from django import forms
from account.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=8, required=True, widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with given email already exists')
        return email

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        return user

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'bio']

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if not name.isalpha():
            raise forms.ValidationError('Firstname can only contain letters')
        return name
    
    def clean_last_name(self):
        name = self.cleaned_data.get('last_name')
        if not name.isalpha():
            raise forms.ValidationError('Last name can only contain letters')
        return name
        