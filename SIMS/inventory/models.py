from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from users.models import User
from django.urls import reverse
import uuid


# from qr_code.qrcode.utils import QRCodeOptions


def user_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# Create your models here.
# Franck's account
class MainUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# Account with read-only rights
class LambdaUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Piece(models.Model):
    ### ITEM SPECIFICATIONS ###

    part_number = models.CharField(max_length=200, help_text='Enter the part_number')
    website = models.URLField(max_length=254, help_text='Enter the part manufacturer website')
    manufacturer = models.CharField(max_length=120, help_text='Enter the manufacturer name')

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

    """Model representing a generic piece"""
    piece_model = models.CharField(max_length=200)
    cae_serialnumber = models.CharField(max_length=120, help_text='Enter the piece serial number')

    # Foreign Key used because piece can only have one category, but categories can have multiple pieces
    # Category as a string rather than object because it hasn't been declared yet in the file
    #category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    description = models.TextField(max_length=1000, help_text='Enter a brief description of the piece')
    documentation = models.CharField(max_length=120, help_text='Enter the piece documentation')

    item_type = models.CharField(max_length=20, choices=TYPE_CHOICE)
    item_characteristic = models.CharField(max_length=20, choices=CHARACTERISTIC_CHOICE)

    def display_category(self):
        """Create a string for the Category. This is required to display category in Admin."""
        return ', '.join(category.part_number for category in self.category.all()[:1])

    display_category.short_description = 'Category'

    def __str__(self):
        """String for representing the Model object."""
        return self.cae_serialnumber

    def get_absolute_url(self):
        """Returns the url to access a detail record for this piece."""
        return reverse('piece-detail', args=[str(self.id)])


class PieceInstance(models.Model):
    """Model representing a specific piece of a part (i.e. that can be moved from the inventory)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='Unique ID for this particular piece across whole inventory')

    instance_number = models.CharField(max_length=120, help_text='Enter the piece serial number')
    piece = models.ForeignKey('Piece', on_delete=models.RESTRICT, null=True)

    LOCATION = (
        ('A1', 'Armoire 1'),
        ('A2', 'Armoire 2'),
        ('A3', 'Armoire 3'),
        ('A4', 'Armoire 4'),
    )

    location = models.CharField(
        max_length=20,
        choices=LOCATION,
        blank=True,
        default='A1',
        help_text='Piece location',
    )

    # Choices for the piece status
    STATUS_CHOICE = (
        ('Reparation', 'Reparation'),
        ('New', 'New'),
        ('Refurbishing', 'Refurbishing'),
        ('U', 'In Use'),
        ('S', 'In Stock')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        blank=True,
        default='New',
        help_text='Piece current status',
    )
    # Choices for the item restriction norm
    RESTRICTION_CHOICE = (
        ('ITAR', 'ITAR'),
        ('Controlled', 'Controlled'),
        ('None', 'Not Application')
    )
    restriction = models.CharField(
        max_length=20,
        choices=RESTRICTION_CHOICE,
        blank=True,
        default='None',
        help_text='Piece restriction access',
    )
    # Choices for the item owner
    OWNER_CHOICE = (
        ('CAE', 'CAE'),
        ('Customer', 'RSAF'),
        ('Other', 'other'),
    )
    owner = models.CharField(
        max_length=20,
        choices=OWNER_CHOICE,
        blank=True,
        default='CAE',
        help_text='Piece owner',
    )

    class Meta:
        ordering = ['location']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id},{self.instance_number}, {self.piece.cae_serialnumber}, {self.location}, {self.owner}, {self.restriction}, {self.status}'

    def display_piece(self):
        """Create a string for the Piece. This is required to display piece in Admin."""
        return ', '.join(piece.cae_serialnumber for piece in self.piece.all()[:1])

    display_piece.short_description = 'Piece'

# Class to have details about spares
# Item class will be used to count them
# Heritage from Item class
# class Spare(Item):
#     # Choices for the item status
#     STATUS_CHOICE = (
#         ('Repaired', 'repaired'),
#         ('New', 'new'),
#         ('Refurbished', 'refurbished'),
#     )
#     # Choices for the item restriction norm
#     RESTRICTION_CHOICE = (
#         ('ITAR', 'itar'),
#         ('Controlled', 'controlled'),
#     )
#     # Choices for the item owner
#     OWNER_CHOICE = (
#         ('CAE', 'cae'),
#         ('Customer', 'customer'),
#         ('Other', 'other'),
#     )
#     spare_current = models.PositiveSmallIntegerField()
#     spare_required = models.PositiveSmallIntegerField()
#     spare_minimum = models.PositiveSmallIntegerField()
#     # entry_date TBD entered once at first entry and never again
#     update_date = models.DateField(auto_now_add=True)  # Automatically set the field to now when the object is updated
#     status = models.CharField(max_length=20, choices=STATUS_CHOICE)
#     obsolescence = models.BooleanField(default=False)
#     PN_replacement = models.SlugField(blank=True, null=True)
#     PN_compatible = models.SlugField(blank=True, null=True)
#     notes = models.TextField(blank=True, null=True)
#     restriction = models.CharField(max_length=20, choices=RESTRICTION_CHOICE)
#     owner = models.CharField(max_length=20, choices=OWNER_CHOICE)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     rspl = models.BooleanField(default=False)
#     life_deadline = models.DateField()
#     cal_recurrence = models.CharField(max_length=10)
#     rec_last_date = models.DateField()
#     rec_next_date = models.DateField()
#     warranty_end = models.DateField()
