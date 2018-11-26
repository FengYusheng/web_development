# -*- coding: utf-8 -*-
from django import forms

from lists.models import Item

EMPTY_LIST_ERROR = "You can't have an empty list item"

# class ItemForm(forms.Form):
#     item_text = forms.CharField(
#         # https://docs.djangoproject.com/en/2.1/ref/forms/widgets/
#         widget=forms.fields.TextInput(
#             attrs={
#                 'placeholder': 'Enter a to-do item',
#                 'class': 'form-control input-lg'
#             }
#         )
#     )


class ItemForm(forms.models.ModelForm):
    # Create a form based on an existing model.
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
                    'placeholder': 'Enter a to-do item',
                    'class': 'form-control input-lg'
                }
            )
        }
        error_messages = {
            'text':{'required':EMPTY_LIST_ERROR}
        }
