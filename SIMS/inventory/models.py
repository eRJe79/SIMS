from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from django.urls import reverse
import uuid


# from qr_code.qrcode.utils import QRCodeOptions


def user_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Piece(models.Model):
    """Model representing a generic piece"""

    # Choices for the item type
    TYPE_CHOICE = (
        ('Original', 'original'),
        ('Simulated', 'simulated'),
        ('Modified', 'modified'),
    )
    # Choices for the item characteristic
    CHARACTERISTIC_CHOICE = (
        ('Sim Part', 'Sim part'),
        ('Consumable', 'consumable'),
        ('Tool', 'tool'),
        ('PPE', 'ppe'),
        ('Office', 'office'),
        ('Building', 'building'),
    )
    # Choices for the item owner
    OWNER_CHOICE = (
        ('CAE', 'CAE'),
        ('Customer', 'RSAF'),
        ('Other', 'other'),
    )
    # Choices for the restriction
    RESTRICTION_CHOICE = (
        ('ITAR', 'ITAR'),
        ('Controlled', 'Controlled'),
        ('None', 'Not Application')
    )

    part_number = models.CharField(max_length=200, help_text='Enter the part_number')
    manufacturer = models.CharField(max_length=120, help_text='Enter the manufacturer name')
    manufacturer_serialnumber = models.CharField(max_length=120, help_text='Enter the piece serial number')
    website = models.URLField(max_length=254, help_text='Enter the part manufacturer website')
    piece_model = models.CharField(max_length=200)


    # Category as a string rather than object because it hasn't been declared yet in the file
    #category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    description = models.TextField(max_length=1000, help_text='Enter a brief description of the piece')
    documentation = models.CharField(max_length=120, help_text='Enter the piece documentation')

    item_type = models.CharField(max_length=20, choices=TYPE_CHOICE)
    item_characteristic = models.CharField(max_length=20, choices=CHARACTERISTIC_CHOICE)

    restriction = models.CharField(
        max_length=20,
        choices=RESTRICTION_CHOICE,
        blank=True,
        default='None',
        help_text='Piece restriction access',
    )

    owner = models.CharField(
        max_length=20,
        choices=OWNER_CHOICE,
        blank=True,
        default='CAE',
        help_text='Piece owner',
    )

    # This is a default return method to access Piece
    def __str__(self):
        """String for representing the Model object."""
        return self.manufacturer_serialnumber

    # This method is used is some templates to have link directed to the piece detail
    def get_absolute_url(self):
        """Returns the url to access a detail record for this piece."""
        return reverse('piece-detail', args=[str(self.id)])


class PieceInstance(models.Model):
    """Model representing a specific piece of a part (i.e. that can be moved from the inventory)."""
    # Choices for the piece status
    STATUS_CHOICE = (
        ('Reparation', 'Reparation'),
        ('New', 'New'),
        ('Refurbishing', 'Refurbishing'),
        ('U', 'In Use'),
        ('S', 'In Stock')
    )
    # Choices for the instance location
    LOCATION = (
        ('Simulator', 'Simulator'),
        ('Bureau', 'Bureau'),
        ('MPDS', 'MPDS'),
        ('PTD', 'PTD'),
        ('ERTMS', 'ERTMS'),
    )

    SECOND_LOCATION = (
        ('Simulator', (
            ('FMS1', 'FMS1'),
            ('FMS2', 'FMS2'),
            ('Hangar', 'Hangar'),
        )),
        ('Bureau', (
            ('Management', 'Management'),
            ('Team A', 'Team A'),
            ('Team B', 'Team B'),
        )),
        ('MPDS', (
            ('MPDS1', 'MPDS1'), ('MPDS2', 'MPDS2'), ('MPDS3', 'MPDS3'), ('MPDS4', 'MPDS4'), ('MPDS5', 'MPDS5'),
            ('MPDS6', 'MPDS6'), ('MPDS7', 'MPDS7'), ('MPDS8', 'MPDS8'), ('MPDS9', 'MPDS9'), ('MPDS10', 'MPDS10'),
        )),
        ('PTD', (
            ('Laptop 1', 'Laptop 1'), ('Laptop 2', 'Laptop 2'),
            ('PTD 1', 'PTD 1'), ('PTD 2', 'PTD 2'), ('PTD 3', 'PTD 3'), ('PTD 4', 'PTD 4'),
        )),
        ('ERTMS', (
            ('ERTMS 1', 'ERTMS 1'), ('ERTMS 2', 'ERTMS 2'),
        )),
    )

    THIRD_LOCATION = (
        ('FMS1', (
            ('IOS', 'IOS'), ('CRVS', 'CRVS'), ('Server Room', 'Server Room'), ('Cockpit', 'Cockpit'),
            ('Compressor Room', 'Compressor Room'),
        )),
        ('FMS2', (
            ('IOS', 'IOS'), ('CRVS', 'CRVS'), ('Server Room', 'Server Room'), ('Cockpit', 'Cockpit'),
            ('Compressor Room', 'Compressor Room'),
        )),
        ('Hangar-SG3', (
                     ('A1', 'A1'), ('A1CB1', 'A1CB1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5'),
                     ('A6', 'A6'), ('A7', 'A7'), ('A8', 'A8'), ('A9', 'A9'), ('A10', 'A10'), ('A10 Bis', 'A10 Bis'),
                     ('A11', 'A11'), ('A20', 'A20'), ('A25', 'A25'), ('A30', 'A30'),
                     ('SS1', 'SS1'), ('SS2', 'SS2'), ('SS3', 'SS3'), ('SS4', 'SS4'), ('SS5', 'SS5'), ('SS6', 'SS6'),
                     ('SS7', 'SS7'),
        )),
    )

    FOURTH_LOCATION = (
        ('IOS', 'IOS'),
        ('CRVS', (
            ('Front center stand', 'Front center stand'), ('Front top stand', 'Front top stand'),
            ('Front right stand', 'Front right stand'), ('Front left stand', 'Front left stand'),
            ('Aft right stand', 'Aft right stand'), ('Aft center stand', 'Aft center stand'),
            ('Aft top stand', 'Aft top stand'), ('Aft left stand', 'Aft left stand'),
            ('Door Mechanism', 'Door Mechanism'),
        )),
        ('Simulator-Simulated Cockpit', (
            ('Seat', 'Seat'), ('Front', 'Front'), ('Aft', 'Aft'),
        )),
        ('Simulator-Other', (
            ('Over Floor', 'Over Floor'), ('Under Floor', 'Under Floor'), ('Structure', 'Structure'),
        )),
        ('Server Room', (
         ('S1', 'S1'),
         ('SG1', 'SG1'),
         ('SG2', 'SG2'),
        )),
    )

    FIFTH_LOCATION = (
        ('S1', (
             ('A3', 'A3'), ('A6', 'A6'), ('A20', 'A20'), ('A35', 'A35'),
             ('A40', 'A40'), ('A44', 'A44'), ('A50', 'A50'), ('A55', 'A55'),
             ('A60', 'A60'), ('A65', 'A65'), ('A70', 'A70'), ('A75', 'A75'),
             ('AB45', 'AB45'), ('AB50', 'AB50'), ('CRA9', 'CRA9'), ('CRA11', 'CRA11'),
             )),
        ('SG1', (
             ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5'),
             ('A6', 'A6'), ('A7', 'A7'), ('A8', 'A8'), ('A10', 'A10'),
             ('A11', 'A11'), ('A12', 'A12'), ('A13', 'A13'), ('A14', 'A14'),
             ('A15', 'A15'), ('A16', 'A16'), ('A17', 'A17'), ('A18', 'A18'),
             ('A19', 'A19'), ('A20', 'A20'), ('A21', 'A21'), ('A22', 'A22'),
             ('A23', 'A23'), ('A24', 'A24'),
             )),
        ('SG2', (
             ('A2', 'A2'), ('A3', 'A3'), ('A8', 'A8'), ('A10', 'A10'),
             ('A11', 'A11'), ('A12', 'A12'), ('A13', 'A13'), ('A14', 'A14'),
             ('A15', 'A15'), ('A16', 'A16'), ('A17', 'A17'), ('A18', 'A18'),
             ('A19', 'A19'), ('A20', 'A20'), ('A21', 'A21'), ('A22', 'A22'),
             ('A23', 'A23'), ('A24', 'A24'), ('A27', 'A27'), ('A28', 'A28'),
             ('A30', 'A30'), ('A32', 'A32'), ('A34', 'A34'), ('A34 Bis', 'A34 Bis'),
             )),
    )
    # Foreign Key used because instance can only have one piece, but pieces can have multiple instances
    piece = models.ForeignKey('Piece', on_delete=models.CASCADE, null=True)
    # Instance specific serial number, setting blank=True as it might not be required
    serial_number = models.CharField(max_length=200, blank=True, help_text='Enter the part_number')

    # Date management
    # Date where the instance is created (set at creation and never updated then)
    date_created = models.DateField(auto_now_add=True)
    # Date of update: this date changes at update and the history is kept - automatic set
    date_update = models.DateField(auto_now=True)
    # Date of the next calibration: to be changes when calibration is done - can be let empty
    date_calibration = models.DateField(blank=True, null=True, help_text='YYYY-MM-DD')
    # Date of end of life: where the instance will end - can be let empty
    date_end_of_life = models.DateField(blank=True, null=True, help_text='YYYY-MM-DD')

    location = models.CharField(
        max_length=20,
        choices=LOCATION,
        blank=True, null=True,
        help_text='Piece location',
    )

    second_location = models.CharField(
        max_length=20,
        default='',
        choices=SECOND_LOCATION,
        blank=True, null=True,
        help_text='Piece second location',
    )

    third_location = models.CharField(
        max_length=20,
        default='',
        choices=THIRD_LOCATION,
        blank=True, null=True,
        help_text='Piece third location',
    )

    fourth_location = models.CharField(
        max_length=20,
        choices=FOURTH_LOCATION,
        default='',
        blank=True, null=True,
        help_text='Piece fourth location',
    )

    fifth_location = models.CharField(
        max_length=20,
        choices=FIFTH_LOCATION,
        default='',
        blank=True, null=True,
        help_text='Piece fifth location',
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        blank=True,
        default='New',
        help_text='Piece current status',
    )

    # Default method to access the PieceInstance
    def __str__(self):
        return self.serial_number





