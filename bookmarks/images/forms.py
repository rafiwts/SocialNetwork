from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
from urllib import request
from .models import Image

class ImageCreateForm(forms.ModelForm): 
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput # choosing an image from an external html, we overwrite the 'url' using HiddenInput - the url field will be hidden
        }
    
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions: # if jpg, jpeg in valid_extensions
            raise forms.ValidationError('The given URL does not ' \
                                        'match valid image extensions.')
        return url
    
    def save(self, force_isert=False,
                   force_update=False,
                   commit=True):
        image = super(ImageCreateForm, self).save(commit=False) # calling a save function without saving to the database
        image_url = self.cleaned_data['url']
        image_name = f'{slugify(image.title)}.{image_url.rsplit(".", 1)[1].lower()}'
        response = request.urlopen(image_url)
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)
        if commit:
            image.save() # it saves only to the database when save = True
        return image