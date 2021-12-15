import datetime
from django.db import models
from simple_history.models import HistoricalRecords
from datetime import date

from django.urls import reverse


def user_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# Defining Location as Classes to have a better object manipulation
class First_location(models.Model):
    """
    Model representing the first level of location
    :param name: Charfield
    """
    name = models.CharField(max_length=30, default='Cazaux')

    class Meta:
        verbose_name_plural = "1. First Location"

    def __str__(self):
        """
        Method to access Location
        :rtype: CharField
        """
        return self.name


class Second_location(models.Model):
    """
    Model representing the second level of location
    :param name: Charfield
    :param previous_loc: ForeignKey
    """
    previous_loc = models.ForeignKey(First_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "2. Second Location"

    def __str__(self):
        """
        Method to access Location
        :rtype: CharField
        """
        return self.name


class Third_location(models.Model):
    """
    Model representing the third level of location
    :param name: Charfield
    :param previous_loc: ForeignKey
    """
    previous_loc = models.ForeignKey(Second_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "3. Third Location"

    def __str__(self):
        """
        Method to access Location
        :rtype: CharField
        """
        return self.name


class Fourth_location(models.Model):
    """
    Model representing the fourth level of location
    :param name: Charfield
    :param previous_loc: ForeignKey
    """
    previous_loc = models.ForeignKey(Third_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "4. Fourth Location"

    def __str__(self):
        """
        Method to access Location
        :rtype: CharField
        """
        return self.name


class Fifth_location(models.Model):
    """
    Model representing the fifth level of location
    :param name: Charfield
    :param previous_loc: ForeignKey
    """
    previous_loc = models.ForeignKey(Fourth_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "5. Fifth Location"

    def __str__(self):
        """
        Method to access Location
        :rtype: CharField
        """
        return self.name


class Sixth_location(models.Model):
    """
    Model representing the sixth level of location
    :param name: Charfield
    :param previous_loc: ForeignKey
    """
    previous_loc = models.ForeignKey(Fifth_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "6. Sixth Location"

    def __str__(self):
        """
        Method to access Location
        :rtype: CharField
        """
        return self.name


class Seventh_location(models.Model):
    """
    Model representing the seventh level of location
    :param name: Charfield
    :param previous_loc: ForeignKey
    """
    previous_loc = models.ForeignKey(Sixth_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "7. Seventh Location"

    def __str__(self):
        """
        Method to access Location
        :rtype: CharField
        """
        return self.name


class Eighth_location(models.Model):
    """
    Model representing the eighth level of location
    :param name: Charfield
    :param previous_loc: ForeignKey
    """
    previous_loc = models.ForeignKey(Seventh_location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "8. Eighth Location"

    def __str__(self):
        """
        Method to access Location
        :rtype: CharField
        """
        return self.name


# Class describing main categories with their specific attribute and pieces
# Example of category : a 500GB Seagate Hard Drive and a 1TB Seagate Hard Drive are 2 different categories
class Piece(models.Model):
    """
    Model representing a Piece
    :param name, manufacturer, manufacturer_part_number, provider, provider_part_number, cae_part_number, piece_model,
     item_type, item_characteristic : Charfield
    :param description, update_comment: TextField
    :param is_obsolete: BooleanField
    :param website: URLField
    :param documentation: FileField
    :param image: ImageField
    :param calibration_recurrence: IntegerField
    :param history: HistoricalRecord()
    """

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
    manufacturer_part_number = models.CharField(max_length=200, null=True, blank=True)
    provider = models.CharField(max_length=120, null=True, blank=True)
    provider_part_number = models.CharField(max_length=200, null=True, blank=True)
    cae_part_number = models.CharField(max_length=200)
    name = models.CharField(max_length=120, null=True, blank=True)
    website = models.URLField(max_length=254, null=True, blank=True)
    piece_model = models.CharField(max_length=200, null=True, blank=True)

    is_obsolete = models.BooleanField(default=False)  # Franck's account

    description = models.TextField(max_length=1000, null=True, blank=True)
    documentation = models.FileField(upload_to='documents/documentation/', blank=True, null=True)
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
        return self.name

    # This method is used is some templates to have link directed to the piece detail
    def get_absolute_url(self):
        """Returns the url to access a detail record for this piece."""
        return reverse('piece-detail', args=[str(self.id)])

    # This method is used is some templates to get calibration reccurence in days
    def get_calibration_recurrence(self):
        """Returns the calibration reccurence days this piece."""
        return self.calibration_recurrence

    def get_history(self):
        """
        Retrieve the three last history input of the object
        :rtype: list
        """
        history = self.history.all()
        # we get only the three last history iterations
        if len(history) == 1:
            myhistory = history
        elif len(history) == 2:
             myhistory = (history[0], history[1])
        else:
             myhistory = (history[0], history[1], history[2])
        print(len(history))
        return myhistory


# Used to create groups of Pieces that will be equivalent between them
class Equivalence(models.Model):
    """
    Model representing an Equivalence between several Pieces
    :param name: Charfield
    :param pieceeq_1, pieceeq_2, pieceeq_3, pieceeq_4, pieceeq_5, pieceeq_6, pieceeq_7, pieceeq_8, pieceeq_9,
     pieceeq_10, pieceeq_11, pieceeq_12, pieceeq_13, pieceeq_14, pieceeq_15: ForeignKey
    """
    name = models.CharField(max_length=120, null=False, blank=False)
    pieceeq_1 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_1', null=True, blank=True)
    pieceeq_2 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_2',  null=True, blank=True)
    pieceeq_3 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_3',  null=True, blank=True)
    pieceeq_4 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_4',  null=True, blank=True)
    pieceeq_5 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_5',  null=True, blank=True)
    pieceeq_6 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_6',  null=True, blank=True)
    pieceeq_7 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_7',  null=True, blank=True)
    pieceeq_8 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_8',  null=True, blank=True)
    pieceeq_9 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_9',  null=True, blank=True)
    pieceeq_10 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_10',  null=True, blank=True)
    pieceeq_11 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_11',  null=True, blank=True)
    pieceeq_12 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_12',  null=True, blank=True)
    pieceeq_13 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_13',  null=True, blank=True)
    pieceeq_14 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_14',  null=True, blank=True)
    pieceeq_15 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pieceeq_15',  null=True, blank=True)

    # This is a default return method to access Piece
    def __str__(self):
        """
        Method to access Equivalence
        :rtype: CharField
        """
        return self.name

    # This method is used  to have link directed to the equivalence detail
    def get_absolute_url(self):
        """
        Method to return specific Equivalence
        :rtype: url
        """
        return reverse('equivalence-detail', args=[str(self.id)])


class GroupAssembly(models.Model):
    """
    Model representing a group of Assemblies
    :param name, kit_partnumber, manufacturer, manufacturer_part_number, provider, provider_part_number: Charfield
    :param date_created: DateField
    :param image: ImageField
    :param update_comment: TextField
    :param history: HistoricalRecord()
    """
    name = models.CharField(max_length=250, blank=False, null=False)
    # Part number is mandatory
    kit_partnumber = models.CharField(max_length=250, blank=False, null=False)
    manufacturer = models.CharField(max_length=120, null=True, blank=True)
    manufacturer_part_number = models.CharField(max_length=200, null=True, blank=True)
    provider = models.CharField(max_length=120, null=True, blank=True)
    provider_part_number = models.CharField(max_length=200, null=True, blank=True)
    # Date where the GA is created (set at creation and never updated then)
    date_created = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    update_comment = models.TextField(default='No comment', max_length=1000, blank=True, null=True)
    # History log
    history = HistoricalRecords()

    # Default method to access the Kit
    def __str__(self):
        """
        Method to access Group Assembly
        :rtype: CharField
        """
        return self.name

    # This method is used is some templates to have link directed to the kit detail
    def get_absolute_url(self):
        """
        Method to return specific Group Assembly
        :rtype: url
        """
        return reverse('groupassembly-detail', args=[str(self.id)])

    def get_kit_children(self):
        """
        Return the list of Assemblies registered in the Group Assembly
        :rtype: list
        """
        return self.kit_set.all()

    def get_history(self):
        """
        Retrieve the three last history input of the object
        :rtype: list
        """
        history = self.history.all()
        # we get only the three last history iterations
        if len(history) == 1:
            myhistory = history
        elif len(history) == 2:
            myhistory = (history[0], history[1])
        else:
            myhistory = (history[0], history[1], history[2])
        print(len(history))
        return myhistory


# Class describing the instance of pieces with their specific attributes and methods
class PieceInstance(models.Model):
    """
    Model representing an Instance of a Piece with their specific attributes and methods
    :param manufacturer_serialnumber, serial_number, provider_serialnumber, status, condition, restriction,
     owner : Charfield
    :param description, update_comment: TextField
    :param is_rspl: BooleanField
    :param date_created: DateField
    :param first_location, second_location, third_location, fourth_location, fifth_location, sixth_location,
    seventh_location, eighth_location, piece, : ForeignKey
    :param date_created, date_update, date_calibration, date_end_of_life, date_guarantee: DateField
    :param history: HistoricalRecord()
    """

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
        ('In Use', 'In Use'),
        ('In Repair', 'In Repair'),
        ('In Stock', 'In Stock'),
        ('Installed', 'Installed'),
        ('Discarded', 'Discarded'),
        ('On Test', 'On Test'),
        ('Received', 'Received'),
        ('Shipped', 'Shipped'),
        ('Waiting', 'Waiting'),
    )
    # Choices for the piece condition
    CONDITIONS_CHOICE = (
        ('Damaged', 'Damaged'),
        ('New', 'New'),
        ('Repaired', 'Repaired')
    )

    # Foreign Key used because instance can only have one piece, but pieces can have multiple instances
    piece = models.ForeignKey('Piece', on_delete=models.CASCADE, null=True, blank=False)
    # Manufacturer and S/N
    manufacturer_serialnumber = models.CharField(max_length=120, blank=True, null=True)
    # Instance specific serial number, setting blank=True as it might not be required
    serial_number = models.CharField(max_length=200, null=True, blank=False)
    # Provider information - an instance of a piece can be bought from different providers
    provider_serialnumber = models.CharField(max_length=120, null=True, blank=True)

    is_rspl = models.BooleanField(default=False)  # Franck's account
    calibration_document = models.FileField(upload_to='documents/calibration', blank=True, null=True)
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
    update_document = models.FileField(upload_to='documents/update/', blank=True, null=True)

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
        default='',
    )

    condition = models.CharField(
        max_length=20,
        choices=CONDITIONS_CHOICE,
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
        """
        Method to access Instance
        :rtype: CharField
        """
        return self.serial_number

    def get_absolute_url(self):
        """
        Method to return specific Instance
        :rtype: url
        """
        return reverse('piece-instance-detail', args=[str(self.id)])

    @property
    def next_calibration(self):
        """
        Method to calculate and return next calibration date
        We calculate the number of days the Instance has been used
        We substract this value to the number of calibration recurrence in days
        We add the result to the actual date, giving us the next calibration date
        :rtype: DateField
        """
        mytemp = date.today() - self.date_created
        if (self.piece.calibration_recurrence):
            days = datetime.timedelta(days=self.piece.calibration_recurrence) - mytemp
            next_calibration = date.today() + days
            return next_calibration
        else:
            pass

    def calibration_days(self):
        """
        Method used to return the number of days until calibration date
        :rtype: DateTimeField
        """
        delta = self.next_calibration - date.today()
        return delta.days

    def is_calibration_due(self):
        """
        Method to check if the calibration is due
        We need this value to check if the calibration is overdue (if the number is lower than 10, then we display the
        coming calibration on the Dashboard)
        :rtype: BooleanField
        """
        calibration_is_due = False
        if(self.next_calibration):
            due_days = self.next_calibration - date.today()
            if due_days < datetime.timedelta(days=10):
                calibration_is_due = True
            else:
                calibration_is_due = False
        return calibration_is_due

    def is_in_reparation(self):
        """
        Method to check if the Instance is in reparation (we just verify status value)
        :rtype: BooleanField
        """
        if self.status == 'In Repair':
            reparation = True
        else:
            reparation = False
        return reparation

    def is_in_waiting(self):
        """
        Method to check if the Instance is in the Waiting Zone (we just verify first_location value)
        :rtype: BooleanField
        """
        if (self.first_location and self.first_location.name == 'Waiting'):
            waiting = True
        else:
            waiting = False
        return waiting

    def time_spent_in_r_instance(self):
        """
        Method to calculate the number of days in total the Instance has spent in Reparation
        We loop through history
        The first time we are In Repair, we establish initial_time which the history date minus the date_created
        When the Instance stops being in Repair, we add the calculated time to amount_spent_in_r
        Repeat until loop is done
        :rtype: DateTimeField
        """
        history = self.history.all()
        initial_time = self.date_created
        amount_spent_in_r = 0
        mysize = len(history)
        myhistory = []
        for i in range(mysize):
            myhistory.append(history[mysize-i-1])
        for h in myhistory:
            if h.status == 'In Repair':
                initial_time = h.history_date.date()
                if initial_time == date.today():
                    amount_spent_in_r = datetime.timedelta(days=1)
                else:
                    amount_spent_in_r = date.today() - initial_time
            else:
                amount_spent_in_r = h.history_date.date() - initial_time
        return amount_spent_in_r.days

    def get_history(self):
        """
        Retrieve the three last history input of the object
        :rtype: list
        """
        history = self.history.all()
        # we get only the three last history iterations
        if len(history) == 1:
            myhistory = history
        elif len(history) == 2:
             myhistory = (history[0], history[1])
        else:
             myhistory = (history[0], history[1], history[2])
        print(len(history))
        return myhistory


class Kit(models.Model):
    """
    Model representing kit (assembly) is an ensemble of instances
    (example a PC contains multiple instances such as RAM bars, HD, or CPU)
    :param name, kit_serialnumber, manufacturer_serialnumber, provider_serialnumber, kit_status : Charfield
    :param description, update_comment: TextField
    :param date_created: DateField
    :param first_location, second_location, third_location, fourth_location, fifth_location, sixth_location,
    seventh_location, eighth_location, pn_1, pn_2, pn_3, pn_4, pn_5, pn_6, pn_7, pn_8, pn_9, pn_10, pn_11, pn_12, pn_13,
     pn_14, pn_15, piece_kit_1, piece_kit_2, piece_kit_3, piece_kit_4, piece_kit_5, piece_kit_6, piece_kit_7,
     piece_kit_8, piece_kit_9, piece_kit_10, piece_kit_11, piece_kit_12, piece_kit_13, piece_kit_14, piece_kit_15
    : ForeignKey
    :param history: HistoricalRecord()
    """
    STATUS_CHOICE = (
        ('In Use', 'In Use'),
        ('In Stock', 'In Stock'),
        ('Installed', 'Installed'),
        ('On Test', 'On Test'),
        ('Waiting', 'Waiting'),
    )
    group_assembly = models.ForeignKey(GroupAssembly, on_delete=models.CASCADE, null=True, blank=False)
    #Name is mandatory
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    # Serial number is mandatory
    kit_serialnumber = models.CharField(max_length=250, blank=False, null=False)
    # Manufacturer and S/N
    manufacturer_serialnumber = models.CharField(max_length=120, blank=True, null=True)
    # Provider information - an instance of a piece can be bought from different providers
    provider_serialnumber = models.CharField(max_length=120, null=True, blank=True)
    # Status
    kit_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        blank=True,
        default='',
    )
    # Date where the assembly is created (set at creation and never updated then)
    date_created = models.DateField(auto_now_add=True)

    # Added PN (link to pieces) for filtering purpose
    pn_1 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_1', null=True, blank=True)
    pn_2 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_2', null=True, blank=True)
    pn_3 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_3', null=True, blank=True)
    pn_4 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_4', null=True, blank=True)
    pn_5 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_5', null=True, blank=True)
    pn_6 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_6', null=True, blank=True)
    pn_7 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_7', null=True, blank=True)
    pn_8 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_8', null=True, blank=True)
    pn_9 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_9', null=True, blank=True)
    pn_10 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_10', null=True, blank=True)
    pn_11 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_11', null=True, blank=True)
    pn_12 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_12', null=True, blank=True)
    pn_13 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_13', null=True, blank=True)
    pn_14 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_14', null=True, blank=True)
    pn_15 = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='pn_15', null=True, blank=True)

    piece_kit_1 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_1', null=True, blank=True)
    piece_kit_2 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_2', null=True, blank=True)
    piece_kit_3 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_3', null=True, blank=True)
    piece_kit_4 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_4', null=True, blank=True)
    piece_kit_5 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_5', null=True, blank=True)
    piece_kit_6 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_6', null=True, blank=True)
    piece_kit_7 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_7', null=True, blank=True)
    piece_kit_8 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_8', null=True, blank=True)
    piece_kit_9 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_9', null=True, blank=True)
    piece_kit_10 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_10', null=True, blank=True)
    piece_kit_11 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_11', null=True, blank=True)
    piece_kit_12 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_12', null=True, blank=True)
    piece_kit_13 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_13', null=True, blank=True)
    piece_kit_14 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_14', null=True, blank=True)
    piece_kit_15 = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, related_name='piece_kit_15', null=True, blank=True)

    first_location = models.ForeignKey(First_location, on_delete=models.SET_NULL, null=True, blank=True)
    second_location = models.ForeignKey(Second_location, on_delete=models.SET_NULL, null=True, blank=True)
    third_location = models.ForeignKey(Third_location, on_delete=models.SET_NULL, null=True, blank=True)
    fourth_location = models.ForeignKey(Fourth_location, on_delete=models.SET_NULL, null=True, blank=True)
    fifth_location = models.ForeignKey(Fifth_location, on_delete=models.SET_NULL, null=True, blank=True)
    sixth_location = models.ForeignKey(Sixth_location, on_delete=models.SET_NULL, null=True, blank=True)
    seventh_location = models.ForeignKey(Seventh_location, on_delete=models.SET_NULL, null=True, blank=True)
    eighth_location = models.ForeignKey(Eighth_location, on_delete=models.SET_NULL, null=True, blank=True)

    update_comment = models.TextField(default='No comment', max_length=1000, blank=True, null=True)
    # History log
    history = HistoricalRecords()
    # Default method to access the Kit
    def __str__(self):
        """
        Default method to access Movement
        :rtype: char
        """
        return self.name

    # This method is used is some templates to have link directed to the kit detail
    def get_absolute_url(self):
        """Returns the url to access a detail record for this kit."""
        return reverse('kit-detail', args=[str(self.id)])

    def get_history(self):
        """
        Retrieve the three last history input of the object
        :rtype: list
        """
        history = self.history.all()
        # we get only the three last history iterations
        if len(history) == 1:
            myhistory = history
        elif len(history) == 2:
             myhistory = (history[0], history[1])
        else:
             myhistory = (history[0], history[1], history[2])
        print(len(history))
        return myhistory


class MovementExchange(models.Model):
    """
    Model representing a movement between two Piece Instance objects
    :param part_number_1, part_number_2, piece_1, piece_2, item_1, item_2, old_first_location, old_second_location,
    old_third_location, old_fourth_location, old_fifth_location, old_sixth_location, old_seventh_location,
    old_eighth_location: ForeignKey
    :param old_status, reference_number: Charfield
    :param revert_button: BooleanFIeld
    :param update_comment_item1, update_comment_item2: TextField
    :param history: HistoricalRecord()
    """
    # Items exchanged is mandatory
    part_number_1 = models.ForeignKey(Piece, on_delete=models.SET_NULL, related_name='part_number_1', null=True, blank=False)
    part_number_2 = models.ForeignKey(Piece, on_delete=models.SET_NULL, related_name='part_number_2', null=True, blank=False)
    piece_1 = models.ForeignKey(Piece, on_delete=models.SET_NULL, related_name='piece_1', null=True, blank=False)
    piece_2 = models.ForeignKey(Piece, on_delete=models.SET_NULL, related_name='piece_2', null=True, blank=False)
    item_1 = models.ForeignKey(PieceInstance, on_delete=models.SET_NULL, related_name='item_1', null=True, blank=False)
    item_2 = models.ForeignKey(PieceInstance, on_delete=models.SET_NULL, related_name='item_2', null=True, blank=False)
    old_first_location = models.ForeignKey(First_location, on_delete=models.SET_NULL, null=True, blank=True)
    old_second_location = models.ForeignKey(Second_location, on_delete=models.SET_NULL, null=True, blank=True)
    old_third_location = models.ForeignKey(Third_location, on_delete=models.SET_NULL, null=True, blank=True)
    old_fourth_location = models.ForeignKey(Fourth_location, on_delete=models.SET_NULL, null=True, blank=True)
    old_fifth_location = models.ForeignKey(Fifth_location, on_delete=models.SET_NULL, null=True, blank=True)
    old_sixth_location = models.ForeignKey(Sixth_location, on_delete=models.SET_NULL, null=True, blank=True)
    old_seventh_location = models.ForeignKey(Seventh_location, on_delete=models.SET_NULL, null=True, blank=True)
    old_eighth_location = models.ForeignKey(Eighth_location, on_delete=models.SET_NULL, null=True, blank=True)
    old_status = models.CharField(max_length=120, blank=True, null=False)
    # Reference number of the Exchange
    reference_number = models.CharField(max_length=120, blank=True, null=False)

    # setting revert button to True by default
    # will be put at False after fist reversion since we can only revert once
    revert_button = models.BooleanField(default=True)

    update_comment_item1 = models.TextField(max_length=1000, blank=True, null=True)
    update_comment_item2 = models.TextField(max_length=1000, blank=True, null=True)
    # History log
    history = HistoricalRecords()

    # Date management
    # Date where the exchange is done (set at creation and never updated then)
    date_created = models.DateField(auto_now_add=True)

    # Default method to access the Kit
    def __str__(self):
        """
        Default method to access Movement
        :rtype: char
        """
        return self.reference_number

    # This method is used is some templates to have link directed to the kit detail
    def get_absolute_url(self):
        """
        Default method to access specific Movement
        :rtype: url
        """
        return reverse('movement-detail', args=[str(self.id)])


class Consumable(models.Model):
    """
    Model representing a piece that can be used on a daily basis.
    :param name, piece_model, cae_part_number, serial_number, manufacturer, manufacturer_part_number,
    manufacturer_serialnumber, provider, provider_part_number, provider_serialnumber, item_type, item_characteristic,
    status, condition, restriction, owner: Charfield
    :param website: URLField
    :param description, documentation, update_comment: TextField
    :param is_rspl: boolean
    :param documentation, update_document: FileField
    :param uploaded_at: DateTimeField
    :param quantity, low_stock_value: BigInteger
    :param date_created, date_update: DateField
    :param first_location, second_location, third_location, fourth_location, fifth_location, sixth_location,
    seventh_location, eighth_location: ForeignKey
    :param history: HistoricalRecord()
    """
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
        ('In Use', 'In Use'),
        ('In Repair', 'In Repair'),
        ('In Stock', 'In Stock'),
        ('Installed', 'Installed'),
        ('Discarded', 'Discarded'),
        ('On Test', 'On Test'),
        ('Received', 'Received'),
        ('Shipped', 'Shipped'),
        ('Waiting', 'Waiting'),
    )
    # Choices for the piece condition
    CONDITIONS_CHOICE = (
        ('Damaged', 'Damaged'),
        ('New', 'New'),
        ('Repaired', 'Repaired')
    )

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

    name = models.CharField(max_length=120, null=True, blank=True)
    piece_model = models.CharField(max_length=200, null=True, blank=True)

    cae_part_number = models.CharField(max_length=200)
    # Instance specific serial number, setting blank=True as it might not be required
    serial_number = models.CharField(max_length=200, null=True, blank=False)

    manufacturer = models.CharField(max_length=120, null=True, blank=True)
    manufacturer_part_number = models.CharField(max_length=200, null=True, blank=True)
    # Manufacturer and S/N
    manufacturer_serialnumber = models.CharField(max_length=120, blank=True, null=True)

    provider = models.CharField(max_length=120, null=True, blank=True)
    provider_part_number = models.CharField(max_length=200, null=True, blank=True)
    # Provider information - an instance of a piece can be bought from different providers
    provider_serialnumber = models.CharField(max_length=120, null=True, blank=True)

    website = models.URLField(max_length=254, null=True, blank=True)

    description = models.TextField(max_length=1000, null=True, blank=True)
    documentation = models.FileField(upload_to='documents/documentation/', blank=True, null=True)

    image = models.ImageField(upload_to='images', null=True, blank=True)

    item_type = models.CharField(max_length=20, null=True, blank=True, choices=TYPE_CHOICE)
    item_characteristic = models.CharField(max_length=20, null=True, blank=True, choices=CHARACTERISTIC_CHOICE)

    is_rspl = models.BooleanField(default=False)  # Franck's account
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Quantity management
    quantity = models.BigIntegerField(default=0)
    low_stock_value = models.BigIntegerField(default=0)

    # Date management
    # Date where the instance is created (set at creation and never updated then)
    date_created = models.DateField(auto_now_add=True)
    # Date of update: this date changes at update and the history is kept - automatic set
    date_update = models.DateField(auto_now=True)

    update_comment = models.TextField(default='No comment', max_length=1000, blank=True, null=True)
    update_document = models.FileField(upload_to='documents/update/', blank=True, null=True)

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
        default='',
    )

    condition = models.CharField(
        max_length=20,
        choices=CONDITIONS_CHOICE,
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

    def __str__(self):
        """
        Default method to access Consumable
        :rtype: char
        """
        return self.name

    # This method is used is some templates to have link directed to the piece instance detail
    def get_absolute_url(self):
        return reverse('consumable-detail', args=[str(self.id)])

    def is_low_stock(self):
        """
        Takes the actual Consumable quantity and checks if it is lower than advised quantity
        Returns Boolean based on result
        :rtype: bool
        """
        if self.quantity <= self.low_stock_value:
            return True
        else:
            return False

    def get_history(self):
        """
        Retrieve the three last history input of the object
        :rtype: list
        """
        history = self.history.all()
        # we get only the three last history iterations
        if len(history) == 1:
            myhistory = history
        elif len(history) == 2:
             myhistory = (history[0], history[1])
        else:
             myhistory = (history[0], history[1], history[2])
        print(len(history))
        return myhistory
