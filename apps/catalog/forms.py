# -*- coding: utf-8 -*-
from django import forms


class CopyProductForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
