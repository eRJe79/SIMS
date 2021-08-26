import datetime

from django import forms
from django.conf import settings
from django.forms import ModelForm, inlineformset_factory, CheckboxInput

from .models import Piece, PieceInstance, Kit, Second_location

class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ['manufacturer', 'provider', 'manufacturer_part_number', 'cae_part_number', 'provider_part_number',
                  'website', 'piece_model', 'description', 'documentation', 'update_comment', 'image',
                  'calibration_recurrence', 'item_type', 'item_characteristic']
        widgets = {
        'manufacturer': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'manufacturer', 'placeholder': 'Enter the manufacturer name'
        }),
        'manufacturer_part_number': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'manufacturer_part_number', 'placeholder': 'Enter the manufacturer PN'
        }),
        'cae_part_number': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'cae_part_number', 'placeholder': 'Enter CAE PN'
        }),
        'provider': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'provider', 'placeholder': 'Enter the OEM'
        }),
        'provider_part_number': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'provider_part_number', 'placeholder': 'Enter the OEM PN'
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
        'update_comment': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'description', 'placeholder': 'Enter a comment'
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
        }


class PieceInstanceForm(forms.ModelForm):
    class Meta:
        model = PieceInstance
        fields = ['piece', 'kit', 'serial_number', 'manufacturer_serialnumber', 'provider_serialnumber', 'owner',
                  'restriction', 'update_comment', 'is_rspl', 'calibration_document', 'date_calibration',
                  'date_end_of_life', 'date_guarantee', 'first_location', 'second_location', 'third_location',
                  'fourth_location', 'fifth_location', 'status']
        labels = {
            'piece': 'Piece',
            'kit': 'Kit',
            'serial_number': 'CAE Serial Number',
            'manufacturer_serialnumber': 'Manufacturer Serial Number',
            'provider_serialnumber': 'OEM Serial Number',
            'owner': 'Owner',
            'restriction': 'Restriction',
            'update_comment': 'Comment',
            'calibration_document': 'Calibration Document',
            'is_rspl': 'RSPL',
            'date_calibration': 'Next Calibration',
            'date_end_of_life': 'End of Life',
            'date_guarantee': 'Guarantee Expiration',
            'first_location': 'First Location',
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
            'provider_serialnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the piece serial number'}),
            'owner': forms.Select(attrs={'class': 'form-select', 'id': 'owner'}),
            'restriction': forms.Select(attrs={'class': 'form-select', 'id': 'restriction'}),
            'update_comment': forms.TextInput(attrs={'class': 'form-control', 'id': 'update_comment'}),
            'is_rspl': forms.CheckboxInput(),
            'date_calibration': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'YYYY-MM-DD'}),
            'date_end_of_life': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'YYYY-MM-DD'}),
            'date_guarantee': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'YYYY-MM-DD'}),
            'first_location': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Location'}),
            'second_location': forms.Select(attrs={'class': 'form-select'}),
            'third_location': forms.Select(attrs={'class': 'form-select'}),
            'fourth_location': forms.Select(attrs={'class': 'form-select'}),
            'fifth_location': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

        # We override the init method to have location choices dependent on each other
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['second_location'].queryset = Second_location.objects.none()

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
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Assembly Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Assembly Description'}),
            'kit_serialnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assembly Serial Number'}),
        }


PieceInstancePieceFormSet = inlineformset_factory(Piece, PieceInstance, form=PieceInstanceForm, extra=10)
PieceInstanceKitFormSet = inlineformset_factory(Kit, PieceInstance, form=PieceInstanceForm, extra=10)



