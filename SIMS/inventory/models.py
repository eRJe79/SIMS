import datetime
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from simple_history.models import HistoricalRecords
from datetime import date

from django.urls import reverse

# from qr_code.qrcode.utils import QRCodeOptions

def user_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# A kit is an ensemble of instances (for example: a PC contains multiple instances such as RAM bars, HD, or CPU)
class Kit(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    kit_serialnumber = models.CharField(max_length=250, blank=False, null=False)

    # Default method to access the Kit
    def __str__(self):
        return self.name

    # This method is used is some templates to have link directed to the kit detail
    def get_absolute_url(self):
       """Returns the url to access a detail record for this kit."""
       return reverse('kit-detail', args=[str(self.id)])


# Class describing main categories with their specific attribute and pieces
# Example of category : a 500GB Seagate Hard Drive and a 1TB Seagate Hard Drive are 2 different categories
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

    # For new row feature
    related_name = 'instance_reverse',

    part_number = models.CharField(max_length=200, null=True, blank=False)
    manufacturer = models.CharField(max_length=120, null=False, blank=True)
    manufacturer_serialnumber = models.CharField(max_length=120, null=True, blank=False)
    website = models.URLField(max_length=254, null=False, blank=True)
    piece_model = models.CharField(max_length=200, blank=True)

    description = models.TextField(max_length=1000, blank=True)
    documentation = models.CharField(max_length=120, blank=True)

    image = models.ImageField(upload_to='images', blank=True)

    item_type = models.CharField(max_length=20, choices=TYPE_CHOICE, blank=True)
    item_characteristic = models.CharField(max_length=20, choices=CHARACTERISTIC_CHOICE, blank=True)

    # Calibration time recurrence - can be let empty
    calibration_recurrence = models.IntegerField(null=True, blank=True)

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

    # Foreign Key used because instance can only have one kit, but kits can have multiple instances from different piece
    # It can be left empty as an instance doesn't necessarily belongs to a kit
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, null=True, blank=True)
    # Instance specific serial number, setting blank=True as it might not be required

    cae_serial_number = models.CharField(max_length=200, blank=True)

    # Provider information - an instance of a piece can be bought from different providers
    provider = models.CharField(max_length=120, blank=True)
    provider_serialnumber = models.CharField(max_length=120, blank=True)

    # Date management
    # Date where the instance is created (set at creation and never updated then)
    date_created = models.DateField(auto_now_add=True)
    # Date of update: this date changes at update and the history is kept - automatic set
    date_update = models.DateField(auto_now=True)
    # Date of the next calibration: to be changes when calibration is done - can be let empty
    date_calibration = models.DateField(blank=True, null=True)
    # Date of end of life: where the instance will end - can be let empty
    date_end_of_life = models.DateField(blank=True, null=True)
    # Guarantee expiration date: where the guarantee will end - can be let empty
    date_guarantee = models.DateField(blank=True, null=True)

    location = models.CharField(
        max_length=20,
        choices=LOCATION,
        blank=True, null=True,
    )

    second_location = models.CharField(
        max_length=20,
        default='',
        choices=SECOND_LOCATION,
        blank=True, null=True,
    )

    third_location = models.CharField(
        max_length=20,
        default='',
        choices=THIRD_LOCATION,
        blank=True, null=True,
    )

    fourth_location = models.CharField(
        max_length=20,
        choices=FOURTH_LOCATION,
        default='',
        blank=True, null=True,
    )

    fifth_location = models.CharField(
        max_length=20,
        choices=FIFTH_LOCATION,
        default='',
        blank=True, null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        blank=True,
        default='New',
    )

    # History log
    history = HistoricalRecords()

    # This is a default return method to access Piece
    def __str__(self):
        """String for representing the Model object."""
        return self.part_number

    # This method is used is some templates to have link directed to the piece detail
    def get_absolute_url(self):
        """Returns the url to access a detail record for this piece."""
        return reverse('piece-detail', args=[str(self.id)])

    # This method is used is some templates to get calibration reccurence in days
    def get_calibration_recurrence(self):
        """Returns the calibration reccurence days this piece."""
        return self.calibration_recurrence

    @property
    def calibration_days(self):
        delta = self.date_calibration - date.today()
        return delta.days

    def is_calibration_due(self):
        due_days = self.date_calibration - date.today() - datetime.timedelta(days=self.calibration_recurrence)
        if due_days < datetime.timedelta(days=0):
            calibration_is_due = True
        else:
            calibration_is_due = False
        return calibration_is_due

    def is_in_reparation(self):
        if self.status == 'Reparation':
            reparation = True
        else:
            reparation = False
        return reparation

    # This function is to check if the FMS1/2 (second_location_) have no missing piece
    # We just check the fourth_location attribute since the specific FMS location are at this level
    # Checks for FMS 1
    # Seat check
    def fms1_seat_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS1' and piece.fourth_location == 'Seat':
                i=i+1
                print(i)
        if i>0:
            return True
        else:
            return False

    # Front check
    def fms1_front_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS 1' and piece.fourth_location == 'Front':
                i=i+1
            if i>0:
                return True
            else:
                return False

    # Aft check
    def fms1_aft_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS 1' and piece.fourth_location == 'Aft':
                i=i+1
            if i>0:
                return True
            else:
                return False

    # Over Floor check
    def fms1_overfloor_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS 1' and piece.fourth_location == 'Over Floor':
                i=i+1
        if i>0:
            return True
        else:
            return False

    # Under Floor check
    def fms1_underfloor_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS 1' and piece.fourth_location == 'Under Floor':
                i=i+1
            if i>0:
                return True
            else:
                return False

    # Structure check
    def fms1_structure_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS 1' and piece.fourth_location == 'Structure':
                i=i+1
            if i>0:
                return True
            else:
                return False


    # Checks for FMS 2
    # Seat check
    def fms2_seat_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS 2' and piece.fourth_location == 'Seat':
                i=i+1
            if i>0:
                return True
            else:
                return False

    # Front check
    def fms2_front_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS 2' and piece.fourth_location == 'Front':
                i=i+1
            if i>0:
                return True
            else:
                return False
    # Aft check
    def fms2_aft_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS 2' and piece.fourth_location == 'Aft':
                i=i+1
            if i>0:
                return True
            else:
                return False
    # Over Floor check
    def fms2_overfloor_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS 2' and piece.fourth_location == 'Over Floor':
                i=i+1
            if i>0:
                return True
            else:
                return False

    # Under Floor check
    def fms2_underfloor_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS 2' and piece.fourth_location == 'Under Floor':
                i=i+1
            if i>0:
                return True
            else:
                return False

    # Structure check
    def fms2_structure_check(self):
        pieces = Piece.objects.all()
        i=0
        for piece in pieces:
            if piece.second_location == 'FMS 2' and piece.fourth_location == 'Structure':
                i=i+1
            if i>0:
                return True
            else:
                return False














