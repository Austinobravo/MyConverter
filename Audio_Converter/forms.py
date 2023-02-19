from django import forms
from .models import *

class FileForm(forms.ModelForm):
    # file = forms.FileField()
    class Meta:
        model = File
        fields = '__all__'
