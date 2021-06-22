import datetime

from django import forms
from django.forms import ModelForm

from .models import Piece, PieceInstance

class MainUserForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))


class LambdaUserForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))


class PieceForm(forms.Form):
    Model = Piece
    fields = ['part_number', 'manufacturer', 'website', 'piece_model', 'cae_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic']
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
    }


class PieceInstanceForm(ModelForm):
    class Meta:
        model = PieceInstance
        fields = '__all__'

class PieceInstanceUpdateForm(forms.ModelForm):
    class Meta:
        model = PieceInstance
        fields = ['piece', 'instance_number', 'location', 'status', 'owner', 'restriction']



