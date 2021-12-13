from django import forms
from django.forms import ModelForm, inlineformset_factory

from .models import Piece, PieceInstance, Kit, MovementExchange, GroupAssembly, Equivalence, Consumable,\
    Second_location, Third_location, Fourth_location, Fifth_location, Sixth_location, Seventh_location, Eighth_location


class PieceForm(forms.ModelForm):
    """
    Logical structure of Piece model
    """
    class Meta:
        model = Piece
        fields = [ 'name', 'cae_part_number', 'manufacturer', 'provider', 'manufacturer_part_number', 'provider_part_number',
                  'website', 'piece_model', 'is_obsolete', 'description', 'documentation', 'update_comment', 'image',
                  'calibration_recurrence', 'item_type', 'item_characteristic']
        widgets = {
        'name': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'name', 'placeholder': 'Enter Name'
        }),
        'cae_part_number': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'cae_part_number', 'placeholder': 'Enter CAE PN'
        }),
        'manufacturer': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'manufacturer', 'placeholder': 'Enter the manufacturer name'
        }),
        'manufacturer_part_number': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'manufacturer_part_number', 'placeholder': 'Enter the manufacturer PN'
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
        'is_obsolete': forms.CheckboxInput(),
        'description': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'description', 'placeholder': 'Enter a brief description of the piece'
        }),
        'documentation': forms.ClearableFileInput(attrs={
            'multiple': True, 'id': 'documentation'
        }),
        'update_comment': forms.TextInput(attrs={
            'class': 'form-control', 'id': 'description', 'placeholder': 'Enter a comment'
        }),
        'calibration_recurrence': forms.NumberInput(attrs={
            'class': 'form-control', 'id': 'calibration_recurrence', 'placeholder': 'Enter calibration recurrence in days'
        }),
        'item_type': forms.Select(attrs={
            'class': 'form-select', 'id': 'item_type'
        }),
        'item_characteristic': forms.Select(attrs={
            'class': 'form-select', 'id': 'item_characteristic'
        }),
        }


class PieceInstanceForm(forms.ModelForm):
    """
    Logical structure of PieceInstance model
    """
    class Meta:
        model = PieceInstance
        fields = ['piece', 'serial_number', 'manufacturer_serialnumber', 'provider_serialnumber', 'owner',
                  'restriction', 'update_comment','update_document', 'is_rspl', 'calibration_document', 'date_calibration',
                  'date_end_of_life', 'date_guarantee', 'first_location', 'second_location', 'third_location',
                  'fourth_location', 'fifth_location', 'sixth_location', 'seventh_location', 'eighth_location',
                  'status', 'condition']
        labels = {
            'piece': 'Piece',
            'serial_number': 'CAE Serial Number',
            'manufacturer_serialnumber': 'Manufacturer Serial Number',
            'provider_serialnumber': 'OEM Serial Number',
            'owner': 'Owner',
            'restriction': 'Restriction',
            'update_comment': 'Update Comment',
            'update_document': 'Additional/Update Document',
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
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the CAE Serial Number'}),
            'provider_serialnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the piece serial number'}),
            'owner': forms.Select(attrs={'class': 'form-select', 'id': 'owner'}),
            'restriction': forms.Select(attrs={'class': 'form-select', 'id': 'restriction'}),
            'update_comment': forms.TextInput(attrs={'class': 'form-control', 'id': 'update_comment'}),
            'update_document': forms.ClearableFileInput(attrs={'multiple': True, 'id': 'update_document'}),
            'calibration_document': forms.ClearableFileInput(attrs={'multiple': True, 'id': 'calibration_document'}),
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
        """
        Overide of the init method to establish hierarchal links between locations
        """
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


class EquivalenceForm(ModelForm):
    """
    Logical structure of Equivalence model
    """
    class Meta:
        model = Equivalence
        fields = ['name', 'pieceeq_1', 'pieceeq_2', 'pieceeq_3', 'pieceeq_4', 'pieceeq_5', 'pieceeq_6',
    'pieceeq_7', 'pieceeq_8', 'pieceeq_9', 'pieceeq_10', 'pieceeq_11', 'pieceeq_12', 'pieceeq_13', 'pieceeq_14', 'pieceeq_15']
        labels = {
            'name': 'name',
            'pieceeq_1': 'Choose Piece',
            'pieceeq_2': 'Choose Piece',
            'pieceeq_3': 'Choose Piece',
            'pieceeq_4': 'Choose Piece',
            'pieceeq_5': 'Choose Piece',
            'pieceeq_6': 'Choose Piece',
            'pieceeq_7': 'Choose Piece',
            'pieceeq_8': 'Choose Piece',
            'pieceeq_9': 'Choose Piece',
            'pieceeq_10': 'Choose Piece',
            'pieceeq_11': 'Choose Piece',
            'pieceeq_12': 'Choose Piece',
            'pieceeq_13': 'Choose Piece',
            'pieceeq_14': 'Choose Piece',
            'pieceeq_15': 'Choose Piece',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'pieceeq_1': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_2': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_3': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_4': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_5': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_6': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_7': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_8': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_9': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_10': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_11': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_12': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_13': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_14': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pieceeq_15': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
        }


class MovementForm(ModelForm):
    """
    Logical structure of Movement model
    """
    class Meta:
        model = MovementExchange
        fields = ['reference_number', 'piece_1', 'part_number_1', 'item_1', 'update_comment_item1', 'piece_2',
                  'part_number_2', 'item_2', 'update_comment_item2']
        labels = {
            'reference_number': 'Reference Number',
            'piece_1': 'Piece Name filter',
            'part_number_1': 'Piece PN filter',
            'item_1': 'OUT',
            'update_comment_item1': 'Reason for item being replaced',
            'piece_2': 'Piece Name filter',
            'part_number_2': 'Piece PN filter',
            'item_2': 'IN',
            'update_comment_item2': 'Reason for item replacing',
        }
        widgets = {
            'reference_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter the Reference Number'}),
            'piece_1': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Item 1 Name piece filter'}),
            'part_number_1': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Item 1 PN piece filter'}),
            'item_1': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose Item 1'}),
            'update_comment_item1': forms.TextInput(attrs={'class': 'form-control', 'id': 'update_comment_item1'}),
            'piece_2': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Item 2 Name piece filter'}),
            'part_number_2': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Item 1 PN piece filter'}),
            'item_2': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose Item 2'}),
            'update_comment_item2': forms.TextInput(attrs={'class': 'form-control', 'id': 'update_comment_item2'}),
        }

    # We override the init method to have instance choices dependent on piece choices
    def __init__(self, *args, **kwargs):
        """
        Overide of the init method to establish hierarchical links between part_number_x and item_x
        piece_x is used to filter Pieces through their name to narrow available part numbers
        part_number_x is used to select the Piece where we want to pick our Piece Instance
        """
        super().__init__(*args, **kwargs)
        self.fields['part_number_1'].queryset = Piece.objects.none()
        self.fields['part_number_2'].queryset = Piece.objects.none()
        self.fields['item_1'].queryset = PieceInstance.objects.none()
        self.fields['item_2'].queryset = PieceInstance.objects.none()

        if 'piece_1' in self.data:
            try:
                piece_id = int(self.data.get('piece_1'))
                my_piece = Piece.objects.get(id=piece_id)
                myname = my_piece.name
                self.fields['part_number_1'].queryset = Piece.objects.filter(name=myname).order_by('cae_part_number')
            except (ValueError, TypeError):
                pass #invalid input, ignore request
        elif self.instance.pk and self.instance.piece_1:
            self.fields['part_number_1'].queryset = self.instance.piece_1.item_1.order_by('cae_part_number')

        if 'part_number_1' in self.data:
            try:
                piece_id = int(self.data.get('part_number_1'))
                self.fields['item_1'].queryset = PieceInstance.objects.filter(piece_id=piece_id).order_by('serial_number')
            except (ValueError, TypeError):
                pass #invalid input, ignore request
        elif self.instance.pk and self.instance.part_number_1:
            self.fields['item_1'].queryset = self.instance.piece_1.item_1.order_by('name')

        if 'piece_2' in self.data:
            try:
                piece_id = int(self.data.get('piece_2'))
                my_piece = Piece.objects.get(id=piece_id)
                myname = my_piece.name
                self.fields['part_number_2'].queryset = Piece.objects.filter(name=myname).order_by('cae_part_number')
            except (ValueError, TypeError):
                pass  # invalid input, ignore request
        elif self.instance.pk and self.instance.piece_2:
            self.fields['part_number_2'].queryset = self.instance.piece_2.item_2.order_by('cae_part_number')

        if 'part_number_2' in self.data:
            try:
                piece_id = int(self.data.get('part_number_2'))
                self.fields['item_2'].queryset = PieceInstance.objects.filter(piece_id=piece_id).order_by(
                    'serial_number')
            except (ValueError, TypeError):
                pass  # invalid input, ignore request
        elif self.instance.pk and self.instance.part_number_2:
            self.fields['item_2'].queryset = self.instance.piece_2.item_2.order_by('name')


class GroupAssemblyForm(ModelForm):
    """
    Logical structure of Group Assembly model
    """
    class Meta:
        model = GroupAssembly
        fields = ['name', 'kit_partnumber', 'update_comment']
        labels = {
            'name': 'Name',
            'kit_partnumber': 'Kit Part Number',
            'update_comment': 'Update Comment',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Group Assembly Name'}),
            'kit_partnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Assembly Part Number'}),
            'update_comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Update Comment'}),
        }


class KitForm(ModelForm):
    """
    Logical structure of Kit model
    """
    class Meta:
        model = Kit
        fields = ['group_assembly', 'name', 'description', 'kit_serialnumber', 'update_comment', 'kit_status', 'first_location',
                  'second_location', 'third_location', 'fourth_location', 'fifth_location', 'sixth_location',
                  'seventh_location', 'eighth_location',
                  'pn_1', 'pn_2', 'pn_3', 'pn_4', 'pn_5', 'pn_6', 'pn_7', 'pn_8', 'pn_9', 'pn_10', 'pn_11', 'pn_12',
                  'pn_13', 'pn_14', 'pn_15',
                  'piece_kit_1', 'piece_kit_2', 'piece_kit_3', 'piece_kit_4', 'piece_kit_5', 'piece_kit_6',
                  'piece_kit_7', 'piece_kit_8', 'piece_kit_9', 'piece_kit_10', 'piece_kit_11', 'piece_kit_12', 'piece_kit_13',
                  'piece_kit_14', 'piece_kit_15'
                  ]
        labels = {
            'group_assembly': 'Group Assembly',
            'name': 'Name',
            'description': 'Description',
            'kit_serialnumber': 'Kit Serial Number',
            'update_comment': 'Update Comment',
            'kit_status': 'Status',
            'first_location': 'First Location',
            'second_location': 'Second Location',
            'third_location': 'Third Location',
            'fourth_location': 'Fourth Location',
            'fifth_location': 'Fifth Location',
            'sixth_location': 'Sixth Location',
            'seventh_location': 'Seventh Location',
            'eighth_location': 'Eighth Location',
            'pn_1': 'Piece to filter', 'pn_2': 'Piece to filter', 'pn_3': 'Piece to filter',
            'pn_4': 'Piece to filter', 'pn_5': 'Piece to filter', 'pn_6': 'Piece to filter',
            'pn_7': 'Piece to filter', 'pn_8': 'Piece to filter', 'pn_9': 'Piece to filter',
            'pn_10': 'Piece to filter', 'pn_11': 'Piece to filter', 'pn_12': 'Piece to filter',
            'pn_13': 'Piece to filter', 'pn_14': 'Piece to filter', 'pn_15': 'Piece to filter',
            'piece_kit_1': 'Choose Instance', 'piece_kit_2': 'Choose Instance', 'piece_kit_3': 'Choose Instance',
            'piece_kit_4': 'Choose Instance', 'piece_kit_5': 'Choose Instance', 'piece_kit_6': 'Choose Instance',
            'piece_kit_7': 'Choose Instance', 'piece_kit_8': 'Choose Instance', 'piece_kit_9': 'Choose Instance',
            'piece_kit_10': 'Choose Instance', 'piece_kit_11': 'Choose Instance', 'piece_kit_12': 'Choose Instance',
            'piece_kit_13': 'Choose Instance', 'piece_kit_14': 'Choose Instance', 'piece_kit_15': 'Choose Instance',
        }
        widgets = {
            'group_assembly': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Group Assembly'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Assembly Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Assembly Description'}),
            'kit_serialnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assembly Serial Number'}),
            'update_comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Update Comment'}),
            'kit_status': forms.Select(attrs={'class': 'form-select'}),
            'first_location': forms.Select(attrs={'class': 'form-select'}),
            'second_location': forms.Select(attrs={'class': 'form-select'}),
            'third_location': forms.Select(attrs={'class': 'form-select'}),
            'fourth_location': forms.Select(attrs={'class': 'form-select'}),
            'fifth_location': forms.Select(attrs={'class': 'form-select'}),
            'sixth_location': forms.Select(attrs={'class': 'form-select'}),
            'seventh_location': forms.Select(attrs={'class': 'form-select'}),
            'eighth_location': forms.Select(attrs={'class': 'form-select'}),
            'pn_1': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_2': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_3': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_4': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_5': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_6': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_7': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_8': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_9': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_10': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_11': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_12': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_13': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_14': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'pn_15': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_1': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_2': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_3': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_4': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_5': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_6': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_7': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_8': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_9': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_10': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_11': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_12': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_13': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_14': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
            'piece_kit_15': forms.Select(attrs={'class': 'form-select', 'placeholder': '--------'}),
        }

        # We override the init method to have location choices dependent on each other

    def __init__(self, *args, **kwargs):
        """
        Overide of the init method to establish hierarchical links between locations
        """
        super().__init__(*args, **kwargs)
        # Location Declaration
        self.fields['second_location'].queryset = Second_location.objects.none()
        self.fields['third_location'].queryset = Third_location.objects.none()
        self.fields['fourth_location'].queryset = Fourth_location.objects.none()
        self.fields['fifth_location'].queryset = Fifth_location.objects.none()
        self.fields['sixth_location'].queryset = Sixth_location.objects.none()
        self.fields['seventh_location'].queryset = Seventh_location.objects.none()
        self.fields['eighth_location'].queryset = Eighth_location.objects.none()

        # Location management
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


class ConsumableForm(forms.ModelForm):
    """
    Logical structure of Consumable model
    """
    class Meta:
        model = Consumable
        fields = ['name', 'cae_part_number', 'serial_number', 'manufacturer', 'manufacturer_part_number',
                  'manufacturer_serialnumber', 'provider', 'provider_part_number', 'provider_serialnumber',
                  'quantity', 'low_stock_value', 'website',
                  'description', 'documentation', 'image',  'item_type', 'item_characteristic', 'is_rspl',
                  'first_location', 'second_location', 'third_location', 'fourth_location', 'fifth_location',
                  'sixth_location', 'seventh_location', 'eighth_location', 'status', 'condition', 'restriction',
                  'owner', 'update_comment', 'update_document']
        labels = {
            'name': 'Name',
            'cae_part_number': 'CAE Part Number',
            'serial_number': 'CAE Serial Number',
            'manufacturer': 'Manufacturer',
            'manufacturer_part_number': 'Manufacturer Part Number',
            'manufacturer_serialnumber': 'Manufacturer Serial Number',
            'provider': 'OEM',
            'provider_part_number': 'OEM Part Number',
            'provider_serialnumber': 'OEM Serial Number',
            'quantity': 'Quantity available',
            'low_stock_value': 'Recommended stock',
            'website': 'Website',
            'description': 'Description',
            'documentation': 'Documentation',
            'item_type': 'Type',
            'item_characteristic': 'Characteristic',
            'is_rspl': 'RSPL',
            'first_location': 'First Location',
            'second_location': 'Second Location',
            'third_location': 'Third Location',
            'fourth_location': 'Fourth Location',
            'fifth_location': 'Fifth Location',
            'sixth_location': 'Sixth Location',
            'seventh_location': 'Seventh Location',
            'eighth_location': 'Eighth Location',
            'status': 'Status',
            'condition': 'Condition',
            'owner': 'Owner',
            'restriction': 'Restriction',
            'update_comment': 'Update Comment',
            'update_document': 'Additional/Update Document'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Name'}),
            'cae_part_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the CAE Part Number'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the CAE Serial Number'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Manufacturer name'}),
            'manufacturer_part_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Manufacturer Part Number'}),
            'manufacturer_serialnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Manufacturer Serial Number'}),
            'provider': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the OEM name'}),
            'provider_part_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the OEM Part Number'}),
            'provider_serialnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the OEM Serial Number'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the available quantity'}),
            'low_stock_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the recommended stock'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.website.com'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a brief description of the piece'}),
            'documentation': forms.ClearableFileInput(attrs={'multiple': True}),
            'item_type': forms.Select(attrs={'class': 'form-select'}),
            'item_characteristic': forms.Select(attrs={'class': 'form-select'}),
            'is_rspl': forms.CheckboxInput(),
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
            'owner': forms.Select(attrs={'class': 'form-select', 'id': 'owner'}),
            'restriction': forms.Select(attrs={'class': 'form-select', 'id': 'restriction'}),
            'update_comment': forms.TextInput(attrs={'class': 'form-control', 'id': 'update_comment'}),
            'update_document': forms.ClearableFileInput(attrs={'multiple': True, 'id': 'update_document'}),
        }

        # We override the init method to have location choices dependent on each other
    def __init__(self, *args, **kwargs):
        """
        Overide of the init method to establish hierarchical links between locations
        """
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


class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

KitGroupAssemblyFormSet = inlineformset_factory(GroupAssembly, Kit, form=KitForm, extra=1)
PieceInstancePieceFormSet = inlineformset_factory(Piece, PieceInstance, form=PieceInstanceForm, extra=1)



