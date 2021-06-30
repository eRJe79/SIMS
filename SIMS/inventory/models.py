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
        ('A1', 'Armoire 1'),
        ('A2', 'Armoire 2'),
        ('A3', 'Armoire 3'),
        ('A4', 'Armoire 4'),
    )

    # Foreign Key used because instance can only have one piece, but pieces can have multiple instances
    piece = models.ForeignKey('Piece', on_delete=models.CASCADE, null=True)
    # Instance specific serial number, setting blank=True as it might be required
    serial_number = models.CharField(max_length=200, blank=True, help_text='Enter the part_number')

    location = models.CharField(
        max_length=20,
        choices=LOCATION,
        blank=True,
        default='A1',
        help_text='Piece location',
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





