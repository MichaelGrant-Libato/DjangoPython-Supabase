from django import forms

class AvatarUploadForm(forms.Form):
    image = forms.ImageField()
