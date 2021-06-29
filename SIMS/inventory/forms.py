import datetime

from django import forms
from django.forms import ModelForm

from .models import Piece, PieceInstance

class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ['part_number', 'manufacturer', 'website', 'piece_model', 'cae_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic','owner', 'restriction', 'location', 'status']
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
        'location': forms.Select(attrs={
            'class': 'form-control', 'id': 'location'
        }),
        'status': forms.Select(attrs={
            'class': 'form-control', 'id': 'status'
        })
        }



class PieceInstanceForm(ModelForm):
    class Meta:
        model = PieceInstance
        fields = ['instance_number', 'piece', 'color']
        labels = {
            'instance_number':'Instance Number',
            'piece':'Piece',
            'color':'Color',
        }
        widgets = {
            'instance_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Piece Instance Number'}),
            'piece': forms.Select(attrs={'class':'form-select', 'placeholder':'Piece'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'}),
        }





