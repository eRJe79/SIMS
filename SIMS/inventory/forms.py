import datetime

from django import forms
from django.conf import settings
from django.forms import ModelForm, inlineformset_factory

from .models import Piece, PieceInstance, Kit

class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ['part_number', 'manufacturer', 'manufacturer_serialnumber', 'website', 'piece_model', 'description',
                  'documentation', 'image', 'calibration_recurrence', 'item_type', 'item_characteristic','owner',
                  'restriction']
        widgets = {
        'part_number': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'part_number', 'placeholder': 'Enter the manufacture part number'
        }),
        'manufacturer': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'manufacturer', 'placeholder': 'Enter the manufacturer name'
        }),
        'manufacturer_serialnumber': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'manufacturer_serialnumber', 'placeholder': 'Enter the piece serial number'
        }),
        'website': forms.URLInput(attrs={
            'class': 'form-control', 'id': 'website', 'placeholder': 'https://www.website.com'
        }),
        'piece_model': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'piece_model'
        }),
        'description': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'description', 'placeholder': 'Enter a brief description of the piece'
        }),
        'documentation': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'documentation', 'placeholder': 'Enter the piece documentation'
        }),
        'calibration_recurrence': forms.NumberInput(attrs={
            'class': 'form-control', 'id': 'calibration_recurrence'
        }),
        'item_type': forms.Select(attrs={
            'class': 'form-select', 'id': 'item_type'
        }),
        'item_characteristic': forms.Select(attrs={
            'class': 'form-select', 'id': 'item_characteristic'
        }),
        'owner': forms.Select(attrs={
            'class': 'form-select', 'id': 'owner'
        }),
        'restriction': forms.Select(attrs={
            'class': 'form-select', 'id': 'restriction'
        }),
        }


class PieceInstanceForm(ModelForm):
    class Meta:
        model = PieceInstance
        fields = ['piece', 'kit', 'serial_number', 'provider', 'provider_serialnumber', 'date_calibration', 'date_end_of_life', 'date_guarantee', 'location', 'second_location', 'third_location', 'fourth_location',
                  'fifth_location', 'status']
        labels = {
            'piece': 'Piece',
            'kit': 'Kit',
            'serial_number': 'Serial Number',
            'provider': 'Provider',
            'provider_serialnumber': 'Provider Serial Number',
            'date_calibration': 'Next Calibration',
            'date_end_of_life': 'End of Life',
            'date_guarantee': 'Guarantee Expiration',
            'location': 'Location',
            'second_location': 'Second Location',
            'third_location': 'Third Location',
            'fourth_location': 'Fourth Location',
            'fifth_location': 'Fifth Location',
            'status': 'Status'
        }
        widgets = {
            'piece': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose Piece'}),
            'kit': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose Kit'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the CAE Serial Number'}),
            'provider': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the provider name'}),
            'provider_serialnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the piece serial number'}),
            'date_calibration': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'YYYY-MM-DD'}),
            'date_end_of_life': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'YYYY-MM-DD'}),
            'date_guarantee': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'YYYY-MM-DD'}),
            'location': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Location'}),
            'second_location': forms.Select(attrs={'class': 'form-select'}),
            'third_location': forms.Select(attrs={'class': 'form-select'}),
            'fourth_location': forms.Select(attrs={'class': 'form-select'}),
            'fifth_location': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class KitForm(ModelForm):
    class Meta:
        model = Kit
        fields = ['name', 'description', 'kit_serialnumber']
        labels = {
            'name': 'Name',
            'description': 'Description',
            'kit_serialnumber': 'Kit Serial Number',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Kit Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Kit Description'}),
            'kit_serialnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kit Serial Number'}),
        }


PieceInstancePieceFormSet = inlineformset_factory(Piece, PieceInstance, form=PieceInstanceForm, extra=1)
PieceInstanceKitFormSet = inlineformset_factory(Kit, PieceInstance, form=PieceInstanceForm, extra=1)



