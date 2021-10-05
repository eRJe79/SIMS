import datetime
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from simple_history.models import HistoricalRecords
from datetime import date
from mptt.models import MPTTModel
from treebeard.mp_tree import MP_Node
from treebeard.al_tree import AL_Node
from treebeard.ns_tree import NS_Node
from treewidget.fields import TreeForeignKey, TreeManyToManyField

from django.urls import reverse

# from qr_code.qrcode.utils import QRCodeOptions

def user_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# Defining Location as Classes to have a better object manipulation
class First_location(models.Model):
    name = models.CharField(max_length=30, default='Cazaux')

    class Meta:
        verbose_name_plural = "1. First Location"

    def __str__(self):
        return self.name

class Second_location(models.Model):
    previous_loc = models.ForeignKey(First_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "2. Second Location"

    def __str__(self):
        return self.name

class Third_location(models.Model):
    previous_loc = models.ForeignKey(Second_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "3. Third Location"

    def __str__(self):
        return self.name

class Fourth_location(models.Model):
    previous_loc = models.ForeignKey(Third_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "4. Fourth Location"

    def __str__(self):
        return self.name

class Fifth_location(models.Model):
    previous_loc = models.ForeignKey(Fourth_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "5. Fifth Location"

    def __str__(self):
        return self.name

class Sixth_location(models.Model):
    previous_loc = models.ForeignKey(Fifth_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "6. Sixth Location"

    def __str__(self):
        return self.name

class Seventh_location(models.Model):
    previous_loc = models.ForeignKey(Sixth_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "7. Seventh Location"

    def __str__(self):
        return self.name

class Eighth_location(models.Model):
    previous_loc = models.ForeignKey(Seventh_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "8. Eighth Location"

    def __str__(self):
        return self.name

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
    # For new row feature
    related_name = 'instance_reverse',

    manufacturer = models.CharField(max_length=120, null=True, blank=True)
    manufacturer_part_number = models.CharField(max_length=200)
    provider = models.CharField(max_length=120, null=True, blank=True)
    provider_part_number = models.CharField(max_length=200, null=True, blank=True)
    cae_part_number = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(max_length=254, null=True, blank=True)
    piece_model = models.CharField(max_length=200, null=True, blank=True)

    description = models.TextField(max_length=1000, null=True, blank=True)
    documentation = models.CharField(max_length=120, null=True, blank=True)
    update_comment = models.TextField(default='No comment', max_length=1000, blank=True, null=True)

    image = models.ImageField(upload_to='images', null=True, blank=True)

    item_type = models.CharField(max_length=20, null=True, blank=True, choices=TYPE_CHOICE)
    item_characteristic = models.CharField(max_length=20, null=True, blank=True, choices=CHARACTERISTIC_CHOICE)

    # Calibration time recurrence - can be let empty
    calibration_recurrence = models.IntegerField(null=True, blank=True)

    # History log
    history = HistoricalRecords()

    # This is a default return method to access Piece
    def __str__(self):
        """String for representing the Model object."""
        return self.cae_part_number

    # This method is used is some templates to have link directed to the piece detail
    def get_absolute_url(self):
        """Returns the url to access a detail record for this piece."""
        return reverse('piece-detail', args=[str(self.id)])

    # This method is used is some templates to get calibration reccurence in days
    def get_calibration_recurrence(self):
        """Returns the calibration reccurence days this piece."""
        return self.calibration_recurrence

# A kit (assembly) is an ensemble of instances (for example: a PC contains multiple instances such as RAM bars, HD, or CPU)
class Kit(models.Model):
    #Name is mandatory
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    # Serial number is mandatory
    kit_serialnumber = models.CharField(max_length=250, blank=False, null=False)

    # Default method to access the Kit
    def __str__(self):
        return self.name

    # This method is used is some templates to have link directed to the kit detail
    def get_absolute_url(self):
        """Returns the url to access a detail record for this kit."""
        return reverse('kit-detail', args=[str(self.id)])


# Class describing the instance of pieces with their specific attributes and methods
class PieceInstance(models.Model):
    """Model representing a specific piece of a part (i.e. that can be moved from the inventory)."""

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

    # Choices for the piece status
    STATUS_CHOICE = (
        ('Reparation', 'Reparation'),
        ('New', 'New'),
        ('Refurbished', 'Refurbished'),
        ('Use', 'In Use'),
        ('Stock', 'In Stock')
    )

    # Foreign Key used because instance can only have one piece, but pieces can have multiple instances
    piece = models.ForeignKey('Piece', on_delete=models.CASCADE, null=True, blank=False)
    # Foreign Key used because instance can only have one kit, but kits can have multiple instances from different piece
    # It can be left empty as an instance doesn't necessarily belongs to a kit
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, null=True, blank=True)
    # Manufacturer and S/N
    manufacturer_serialnumber = models.CharField(max_length=120, blank=True, null=True)
    # Instance specific serial number, setting blank=True as it might not be required
    serial_number = models.CharField(max_length=200, null=True, blank=False)
    # Provider information - an instance of a piece can be bought from different providers
    provider_serialnumber = models.CharField(max_length=120, null=True, blank=True)

    is_rspl = models.BooleanField(default=False)  # Franck's account
    calibration_document = models.FileField(upload_to='documents/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


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

    update_comment = models.TextField(default='No comment', max_length=1000, blank=True, null=True)

    first_location = models.ForeignKey(First_location, on_delete=models.SET_NULL, null=True, blank=True)
    second_location = models.ForeignKey(Second_location, on_delete=models.SET_NULL, null=True, blank=True)
    third_location = models.ForeignKey(Third_location, on_delete=models.SET_NULL, null=True, blank=True)
    fourth_location = models.ForeignKey(Fourth_location, on_delete=models.SET_NULL, null=True, blank=True)
    fifth_location = models.ForeignKey(Fifth_location, on_delete=models.SET_NULL, null=True, blank=True)
    sixth_location = models.ForeignKey(Sixth_location, on_delete=models.SET_NULL, null=True, blank=True)
    seventh_location = models.ForeignKey(Seventh_location, on_delete=models.SET_NULL, null=True, blank=True)
    eighth_location = models.ForeignKey(Eighth_location, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        blank=True,
        default='New',
    )

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

    # History log
    history = HistoricalRecords()

    # Default method to access the PieceInstance
    def __str__(self):
        return self.serial_number

    # This method is used is some templates to have link directed to the piece instance detail
    def get_absolute_url(self):
        """Returns the url to access a detail record for this piece instance."""
        return reverse('piece-instance-detail', args=[str(self.id)])

    @property
    def calibration_days(self):
        delta = self.date_calibration - date.today()
        return delta.days

    def is_calibration_due(self):
        due_days = self.date_calibration - date.today() - datetime.timedelta(days=self.piece.calibration_recurrence)
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


class Mptt(MPTTModel):
    name = models.CharField(max_length=32)
    parent = TreeForeignKey(
        'self', blank=True, null=True, on_delete=models.CASCADE,
        settings={'filtered': True}, help_text='filtered (exclude pk=1 from parent, see admin.py)')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']




