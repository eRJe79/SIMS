import datetime

from django import forms
from django.conf import settings
from django.forms import ModelForm, inlineformset_factory, CheckboxInput

from .models import Piece, PieceInstance, Kit, MovementExchange, Mptt, First_location,\
    Second_location, Third_location, Fourth_location, Fifth_location, Sixth_location, Seventh_location, Eighth_location

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
                  'fourth_location', 'fifth_location', 'sixth_location', 'seventh_location', 'eighth_location',
                  'status', 'condition']
        labels = {
            'piece': 'Piece',
            'kit': 'Kit',
            'serial_number': 'CAE Serial Number',
            'manufacturer_serialnumber': 'Manufacturer Serial Number',
            'provider_serialnumber': 'OEM Serial Number',
            'owner': 'Owner',
            'restriction': 'Restriction',
            'update_comment': 'Update Comment',
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
            'sixth_location': 'Sixth Location',
            'seventh_location': 'Seventh Location',
            'eighth_location': 'Eighth Location',
            'status': 'Status',
            'condition': 'Condition'
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
            'first_location': forms.Select(attrs={'class': 'form-select'}),
            'second_location': forms.Select(attrs={'class': 'form-select'}),
            'third_location': forms.Select(attrs={'class': 'form-select'}),
            'fourth_location': forms.Select(attrs={'class': 'form-select'}),
            'fifth_location': forms.Select(attrs={'class': 'form-select'}),
            'sixth_location': forms.Select(attrs={'class': 'form-select'}),
            'seventh_location': forms.Select(attrs={'class': 'form-select'}),
            'eighth_location': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
        }

        # We override the init method to have location choices dependent on each other
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['second_location'].queryset = Second_location.objects.none()
        self.fields['third_location'].queryset = Third_location.objects.none()
        self.fields['fourth_location'].queryset = Fourth_location.objects.none()
        self.fields['fifth_location'].queryset = Fifth_location.objects.none()
        self.fields['sixth_location'].queryset = Sixth_location.objects.none()
        self.fields['seventh_location'].queryset = Seventh_location.objects.none()
        self.fields['eighth_location'].queryset = Eighth_location.objects.none()

        if 'first_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('first_location'))
                self.fields['second_location'].queryset = Second_location.objects.filter(previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass #invalid input, ignore request
        elif self.instance.pk and self.instance.first_location:
            self.fields['second_location'].queryset = self.instance.first_location.second_location_set.order_by('name')

        if 'second_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('second_location'))
                self.fields['third_location'].queryset = Third_location.objects.filter(previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass #invalid input, ignore request
        elif self.instance.pk and self.instance.second_location:
            self.fields['third_location'].queryset = self.instance.second_location.third_location_set.order_by('name')

        if 'third_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('third_location'))
                self.fields['fourth_location'].queryset = Fourth_location.objects.filter(previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass #invalid input, ignore request
        elif self.instance.pk and self.instance.third_location:
            self.fields['fourth_location'].queryset = self.instance.third_location.fourth_location_set.order_by('name')

        if 'fourth_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('fourth_location'))
                self.fields['fifth_location'].queryset = Fifth_location.objects.filter(previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass #invalid input, ignore request
        elif self.instance.pk and self.instance.fourth_location:
            self.fields['fifth_location'].queryset = self.instance.fourth_location.fifth_location_set.order_by('name')

        if 'fifth_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('fifth_location'))
                self.fields['sixth_location'].queryset = Sixth_location.objects.filter(previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass #invalid input, ignore request
        elif self.instance.pk and self.instance.fifth_location:
            self.fields['sixth_location'].queryset = self.instance.fifth_location.sixth_location_set.order_by('name')

        if 'sixth_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('sixth_location'))
                self.fields['seventh_location'].queryset = Seventh_location.objects.filter(previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass #invalid input, ignore request
        elif self.instance.pk and self.instance.sixth_location:
            self.fields['seventh_location'].queryset = self.instance.sixth_location.seventh_location_set.order_by('name')

        if 'seventh_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('seventh_location'))
                self.fields['eighth_location'].queryset = Eighth_location.objects.filter(previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass #invalid input, ignore request
        elif self.instance.pk and self.instance.seventh_location:
            self.fields['eighth_location'].queryset = self.instance.seventh_location.eighth_location_set.order_by('name')


class MovementForm(ModelForm):
    class Meta:
        model = MovementExchange
        fields = ['reference_number', 'item_1', 'item_2', 'update_comment']
        labels = {
            'reference_number': 'Reference Number',
            'item_1': 'Item 1',
            'item_2': 'Item 2',
            'update_comment': 'Update Comment'
        }
        widgets = {
            'item_1': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose Item 1'}),
            'item_2': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose Item 2'}),
            'reference_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter the Reference Number'}),
            'update_comment': forms.TextInput(attrs={'class': 'form-control', 'id': 'update_comment'}),
        }


class KitForm(ModelForm):
    class Meta:
        model = Kit
        fields = ['name', 'description', 'kit_serialnumber', 'update_comment', 'first_location', 'second_location',
                  'third_location', 'fourth_location', 'fifth_location', 'sixth_location', 'seventh_location',
                  'eighth_location']
        labels = {
            'name': 'Name',
            'description': 'Description',
            'kit_serialnumber': 'Kit Serial Number',
            'update_comment': 'Update Comment',
            'first_location': 'First Location',
            'second_location': 'Second Location',
            'third_location': 'Third Location',
            'fourth_location': 'Fourth Location',
            'fifth_location': 'Fifth Location',
            'sixth_location': 'Sixth Location',
            'seventh_location': 'Seventh Location',
            'eighth_location': 'Eighth Location',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Assembly Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Assembly Description'}),
            'kit_serialnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assembly Serial Number'}),
            'update_comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Update Comment'}),
            'first_location': forms.Select(attrs={'class': 'form-select'}),
            'second_location': forms.Select(attrs={'class': 'form-select'}),
            'third_location': forms.Select(attrs={'class': 'form-select'}),
            'fourth_location': forms.Select(attrs={'class': 'form-select'}),
            'fifth_location': forms.Select(attrs={'class': 'form-select'}),
            'sixth_location': forms.Select(attrs={'class': 'form-select'}),
            'seventh_location': forms.Select(attrs={'class': 'form-select'}),
            'eighth_location': forms.Select(attrs={'class': 'form-select'}),
        }

        # We override the init method to have location choices dependent on each other

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['second_location'].queryset = Second_location.objects.none()
        self.fields['third_location'].queryset = Third_location.objects.none()
        self.fields['fourth_location'].queryset = Fourth_location.objects.none()
        self.fields['fifth_location'].queryset = Fifth_location.objects.none()
        self.fields['sixth_location'].queryset = Sixth_location.objects.none()
        self.fields['seventh_location'].queryset = Seventh_location.objects.none()
        self.fields['eighth_location'].queryset = Eighth_location.objects.none()

        if 'first_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('first_location'))
                self.fields['second_location'].queryset = Second_location.objects.filter(
                    previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input, ignore request
        elif self.instance.pk and self.instance.first_location:
            self.fields['second_location'].queryset = self.instance.first_location.second_location_set.order_by('name')

        if 'second_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('second_location'))
                self.fields['third_location'].queryset = Third_location.objects.filter(
                    previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input, ignore request
        elif self.instance.pk and self.instance.second_location:
            self.fields['third_location'].queryset = self.instance.second_location.third_location_set.order_by('name')

        if 'third_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('third_location'))
                self.fields['fourth_location'].queryset = Fourth_location.objects.filter(
                    previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input, ignore request
        elif self.instance.pk and self.instance.third_location:
            self.fields['fourth_location'].queryset = self.instance.third_location.fourth_location_set.order_by('name')

        if 'fourth_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('fourth_location'))
                self.fields['fifth_location'].queryset = Fifth_location.objects.filter(
                    previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input, ignore request
        elif self.instance.pk and self.instance.fourth_location:
            self.fields['fifth_location'].queryset = self.instance.fourth_location.fifth_location_set.order_by('name')

        if 'fifth_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('fifth_location'))
                self.fields['sixth_location'].queryset = Sixth_location.objects.filter(
                    previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input, ignore request
        elif self.instance.pk and self.instance.fifth_location:
            self.fields['sixth_location'].queryset = self.instance.fifth_location.sixth_location_set.order_by('name')

        if 'sixth_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('sixth_location'))
                self.fields['seventh_location'].queryset = Seventh_location.objects.filter(
                    previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input, ignore request
        elif self.instance.pk and self.instance.sixth_location:
            self.fields['seventh_location'].queryset = self.instance.sixth_location.seventh_location_set.order_by(
                'name')

        if 'seventh_location' in self.data:
            try:
                previous_loc_id = int(self.data.get('seventh_location'))
                self.fields['eighth_location'].queryset = Eighth_location.objects.filter(
                    previous_loc_id=previous_loc_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input, ignore request
        elif self.instance.pk and self.instance.seventh_location:
            self.fields['eighth_location'].queryset = self.instance.seventh_location.eighth_location_set.order_by(
                'name')

PieceInstancePieceFormSet = inlineformset_factory(Piece, PieceInstance, form=PieceInstanceForm, extra=1)
PieceInstanceKitFormSet = inlineformset_factory(Kit, PieceInstance, form=PieceInstanceForm, extra=1)



