# -*- coding: utf-8 -*-
from django import forms
from common.widget import AdminImageWidget, MultipleInput
# from flatcontent.models import FlatContent
from .models import Photo


# class FlatContentForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorWidget)

# class Meta:
#     model = FlatContent


class ImageForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'main_image', 'title', )
        widgets = {
            'image': AdminImageWidget,
        }


class SearchForm(forms.Form):
    query_field = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super(SearchForm,self).__init__(*args, **kwargs)
        self.fields['query_field'].widget.attrs['class'] = 'form-text autocomplete-search-text'
