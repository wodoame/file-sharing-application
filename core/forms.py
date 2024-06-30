from django import forms
from .models import File, Folder

class UploadFileForm(forms.ModelForm):
    class Meta: 
        model = File
        fields = '__all__'

class CreateFolderForm(forms.ModelForm):
    class Meta: 
        model = Folder
        fields = '__all__'