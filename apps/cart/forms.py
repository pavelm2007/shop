# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.contenttypes.models import ContentType

from django.template.defaultfilters import striptags


from .models import Order, OrderItem, Contact_info

BASKET_OPTIONS_USE_KEEP = False


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem

    content_type = forms.ModelChoiceField(queryset=ContentType.objects.all(),
                                          widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    if BASKET_OPTIONS_USE_KEEP:
        keep = forms.BooleanField(initial=True, required=False)

    def save(self, *args, **kwargs):
        if BASKET_OPTIONS_USE_KEEP:
            if not self.cleaned_data.get('keep', False):
                self.cleaned_data['quantity'] = 0
        self.instance.order.set_quantity(self.instance.content_object,
                                         self.cleaned_data.get('quantity', 0))


OrderFormset = inlineformset_factory(Order, OrderItem, extra=0,
                                     can_delete=False, form=OrderItemForm)


class DefaultOrderForm(forms.ModelForm):
    # name = forms.CharField(label=u'Имя', max_length=100, required=True)
    # phone = forms.CharField(label=u'Телефон', max_length=100, required=True)
    # email = forms.CharField(label=u'E-mail', max_length=100, required=True)
    # comment = forms.CharField(label=u'Комментарий к заказу', max_length=255,
    #                           widget=forms.Textarea(), required=True)

    def __init__(self, *args, **kwargs):
        super(DefaultOrderForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['cols'] = '35'
        self.fields['comment'].widget.attrs['rows'] = '5'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'filed-znach-text'
        if self.errors:

                # bf_errors = self.error_class(error for error in bf.errors]) # Escape and cache in local variable.


            for field, key in self.fields.iteritems():
                error_text = u''

                for i, j in self.errors.iteritems():
                    if field == i:
                        error_text += unicode(striptags(j))
                self.fields[field].initial = None
                # self.fields[field].widget.attrs['value'] = error_text
                self.fields[field].widget.attrs['placeholder'] = error_text
    class Meta:
        model = Contact_info
        exclude = ('order',)

# class DefaultOrderForm(forms.Form):
#     name = forms.CharField(label=u'Имя', max_length=100,required=True)
#     phone = forms.CharField(label=u'Телефон', max_length=100,required=True)
#     email = forms.CharField(label=u'E-mail', max_length=100,required=True)
#     # address = forms.CharField(label=_('Delivery address'), max_length=255)
#     # contact_time = forms.CharField(label=_('Convenient time to call'),
#     #     max_length=50, required=False)
#     comment = forms.CharField(label=u'Комментарий к заказу', max_length=255,
#         widget=forms.Textarea(), required=True)
#
#     def __init__(self, request, *args, **kwargs):
#         super(DefaultOrderForm, self).__init__(*args, **kwargs)
#         self.fields['comment'].widget.attrs['cols'] = '35'
#         self.fields['comment'].widget.attrs['rows'] = '5'
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'filed-znach-text'
