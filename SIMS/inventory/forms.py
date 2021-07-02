import datetime

from django import forms
from django.forms import ModelForm

from .models import Piece, PieceInstance

class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ['part_number', 'manufacturer', 'manufacturer_serialnumber', 'website', 'piece_model', 'description', 'documentation', 'item_type', 'item_characteristic','owner', 'restriction']
        widgets = {
        'part_number': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'part_number'
        }),
        'manufacturer': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'manufacturer'
        }),
        'manufacturer_serialnumber': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'manufacturer_serialnumber'
        }),
        'website': forms.URLInput(attrs={
            'class': 'form-control', 'id': 'website'
        }),
        'piece_model': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'piece_model'
        }),
        'description': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'description'
        }),
        'documentation': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'documentation'
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
        fields = ['piece', 'serial_number', 'location', 'second_location', 'third_location', 'fourth_location',
                  'fifth_location', 'status']
        labels = {
            'piece': 'Piece',
            'serial_number': 'Serial Number',
            'location': 'Location',
            'second_location': 'Second Location',
            'third_location': 'Third Location',
            'fourth_location': 'Fourth Location',
            'fifth_location': 'Fifth Location',
            'status': 'Status'
        }
        widgets = {
            'piece': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Piece'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'location': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Location'}),
            'second_location': forms.Select(attrs={'class': 'form-select', 'placeholder': ' Second Location'}),
            'third_location': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Third Location'}),
            'fourth_location': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Fourth Location'}),
            'fifth_location': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Fifth Location'}),
            'status': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Status'}),
        }





