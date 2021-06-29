import datetime

from django import forms
from django.forms import ModelForm

from .models import Piece, PieceInstance

class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ['part_number', 'manufacturer', 'website', 'piece_model', 'cae_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic','owner', 'restriction']
        widgets = {
        'part_number': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'part_number'
        }),
        'manufacturer': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'manufacturer'
        }),
        'website': forms.URLInput(attrs={
            'class': 'form-control', 'id': 'website'
        }),
        'piece_model': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'piece_model'
        }),
        'cae_serialnumber': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'cae_serialnumber'
        }),
        'description': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'description'
        }),
        'documentation': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'documentation'
        }),
        'item_type': forms.Select(attrs={
            'class': 'form-control', 'id': 'item_type'
        }),
        'item_characteristic': forms.Select(attrs={
            'class': 'form-control', 'id': 'item_characteristic'
        }),
        'owner': forms.Select(attrs={
            'class': 'form-control', 'id': 'owner'
        }),
        'restriction': forms.Select(attrs={
            'class': 'form-control', 'id': 'restriction'
        }),
        }



class PieceInstanceForm(ModelForm):
    class Meta:
        model = PieceInstance
        fields = ['piece', 'location', 'status']
        labels = {
            'piece': 'Piece',
            'location': 'Location',
            'status': 'Status'
        }
        widgets = {
            'piece': forms.Select(attrs={'class':'form-select', 'placeholder': 'Piece'}),
            'location': forms.Select(attrs={'class':'form-select', 'placeholder': 'Location'}),
            'status': forms.Select(attrs={'class':'form-select', 'placeholder': 'Status'}),
        }





