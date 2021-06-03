from django.db import models
from users.models import User


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


# This class describes an article
#class Article(models.Model):
    ### MANUFACTURER SPECIFICATION ###
    #manufacturer = models.CharField(max_length=120)
    # manufacturer_partnumber  = models.SlugField()
    # manufacturer_serienumber = models.SlugField()
    #manufacturer_date = models.DateField(auto_now_add=True)
    #website = models.URLField(max_length=254)

    ### CONTRACTOR SPECIFICATION ###
    #contractor = models.CharField(max_length=120)

    # contractor_partnumber = models.SlugField()
    # contractor_serienumber = models.SlugField()

    ### ARTICLE SPECIFICATION ###
    # part_number = models.SlugField()

    #def __str__(self):
     #   return self.name


# This class describes an item
# Heritage from Original_Manufacturer, Contractor, Article, LocationTree and History
# Original_Manufacturer, Contractor, Article, LocationTree, History
class Item(models.Model):
    ### LOCATION SPECIFICATION ###
    # principal_location = models.CharField(max_length=100)
    ### HISTORY SPECIFICATION ###
    # record      = models.TextField(blank=True, null=True)
    # username    = models.OneToOneField(User, on_delete=models.CASCADE)
    record_date = models.DateField(
        auto_now_add=True)  # Automatically set the field to now when the object is first created
    ### ITEM SPECIFICATIONS ###
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
    ### MANUFACTURER SPECIFICATION ###
    manufacturer = models.CharField(max_length=120)
    # manufacturer_partnumber  = models.SlugField()
    # manufacturer_serienumber = models.SlugField()
    manufacturer_date = models.DateField(auto_now_add=True)
    website = models.URLField(max_length=254)

    ### CONTRACTOR SPECIFICATION ###
    contractor = models.CharField(max_length=120)

    # contractor_partnumber = models.SlugField()
    # contractor_serienumber = models.SlugField()

    ### ARTICLE SPECIFICATION ###
    # part_number = models.SlugField()

    ### ITEM SPECIFICATION ###
    cae_partname = models.CharField(max_length=120)
    # cae_partnumber      = models.SlugField()
    # cae_serienumber     = models.SlugField()
    item_model = models.CharField(max_length=120)

    # description         = models.TextField(blank=True, null=True)
    # comment             = models.TextField(blank=True, null=True)
    # documentation       = models.TextField(blank=True, null=True)
    # item_image          = models.ImageField(upload_to=user_image_path)
    # item_type           = models.CharField(max_length=20, choices=TYPE_CHOICE)
    # item_characteristic = models.CharField(max_length=20, choices=CHARACTERISTIC_CHOICE)
    # IsConsumable        = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    #def __init__(self, manufacturer, manufacturer_date, website, contractor):
    #    self.manufacturer = manufacturer
    #    self.manufacturer_date = manufacturer_date
    #    self.website = website
    #    self.contractor = contractor


# Class to have details about spares
# Item class will be used to count them
# Heritage from Item class
class Spare(Item):
    # Choices for the item status
    STATUS_CHOICE = (
        ('Repaired', 'repaired'),
        ('New', 'new'),
        ('Refurbished', 'refurbished'),
    )
    # Choices for the item restriction norm
    RESTRICTION_CHOICE = (
        ('ITAR', 'itar'),
        ('Controlled', 'controlled'),
    )
    # Choices for the item owner
    OWNER_CHOICE = (
        ('CAE', 'cae'),
        ('Customer', 'customer'),
        ('Other', 'other'),
    )
    spare_current = models.PositiveSmallIntegerField()
    spare_required = models.PositiveSmallIntegerField()
    spare_minimum = models.PositiveSmallIntegerField()
    # entry_date TBD entered once at first entry and never again
    update_date = models.DateField(auto_now_add=True)  # Automatically set the field to now when the object is updated
    status = models.CharField(max_length=20, choices=STATUS_CHOICE)
    obsolescence = models.BooleanField(default=False)
    PN_replacement = models.SlugField(blank=True, null=True)
    PN_compatible = models.SlugField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    restriction = models.CharField(max_length=20, choices=RESTRICTION_CHOICE)
    owner = models.CharField(max_length=20, choices=OWNER_CHOICE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rspl = models.BooleanField(default=False)
    life_deadline = models.DateField()
    cal_recurrence = models.CharField(max_length=10)
    rec_last_date = models.DateField()
    rec_next_date = models.DateField()
    warranty_end = models.DateField()
