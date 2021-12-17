import csv
import datetime


from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView,  CreateView
from django.db.models import Q

import pandas as pd

from .models import (
    Consumable, Equivalence, Piece, PieceInstance, GroupAssembly, Kit,
    First_location, Second_location, Third_location, Fourth_location, Fifth_location, Sixth_location, Seventh_location,
    Eighth_location,
    MovementExchange,
)

from .forms import (
    ConsumableForm, PieceForm, PieceInstanceForm, PieceInstancePieceFormSet, KitGroupAssemblyFormSet, GroupAssemblyForm,
    KitForm, MovementForm, EquivalenceForm,
)


# Movement dependencies management
def load_pn_item_1(request):
    """
    Method used in Movement creation to get Piece list filtered by cae_part_number
    :rtype: list
    """
    piece_id = request.GET.get('piece')
    my_piece = Piece.objects.get(id=piece_id)
    myname = my_piece.name
    myitems = Piece.objects.filter(name=myname).order_by('cae_part_number')
    return render(request, 'hr/part_number_dropdown_list_options.html', {'items': myitems})


def load_item_1(request):
    """
    Method used in Movement creation to get Piece Instance list filtered by serial_number
    :rtype: list
    """
    piece_id = request.GET.get('part_number_1')
    myitems = PieceInstance.objects.filter(piece_id=piece_id).order_by('serial_number')
    # We don't want items that are in stock
    items = []
    for item in myitems:
        if item.status != 'In Stock':
            items.append(item)
    return render(request, 'hr/item_dropdown_list_options.html', {'items': items})


def load_pn_item_2(request):
    """
    Method used in Movement creation to get Piece list filtered by cae_part_number
    :rtype: list
    """
    piece_id = request.GET.get('piece')
    my_piece = Piece.objects.get(id=piece_id)
    myname = my_piece.name
    myitems = Piece.objects.filter(name=myname).order_by('cae_part_number')
    return render(request, 'hr/part_number_dropdown_list_options.html', {'items': myitems})


def load_item_2(request):
    """
    Method used in Movement creation to get Piece Instance list filtered by serial_number
    :rtype: list
    """
    piece_id = request.GET.get('part_number_2')
    myitems = PieceInstance.objects.filter(piece_id=piece_id).order_by('serial_number')
    items = myitems.filter(Q(status='In Stock') | Q(status = 'On Test'))
    return render(request, 'hr/item_dropdown_list_options.html', {'items': items})


def load_piece_kit(request):
    """
    Method used in Assembly creation/update/clone to get Piece Instance list filtered by serial_number
    :rtype: list
    """
    piece_id = request.GET.get('piece')
    items = PieceInstance.objects.filter(piece_id=piece_id).order_by('serial_number')
    return render(request, 'hr/item_dropdown_list_options.html', {'items': items})


# Location dependencies management
def load_second_location(request):
    """
    Method used in Location Management to get second location based on first location choice
    :rtype: list
    """
    first_loc_id = request.GET.get('previous_loc')
    second_loc = Second_location.objects.filter(previous_loc_id=first_loc_id).order_by('name')
    return render(request, 'hr/second_loc_dropdown_list_options.html', {'second_loc': second_loc})


def load_third_location(request):
    """
    Method used in Location Management to get third location based on second location choice
    :rtype: list
    """
    second_loc_id = request.GET.get('previous_loc')
    third_loc = Third_location.objects.filter(previous_loc_id=second_loc_id).order_by('name')
    return render(request, 'hr/third_loc_dropdown_list_options.html', {'third_loc': third_loc})


def load_fourth_location(request):
    """
    Method used in Location Management to get fourth location based on third location choice
    :rtype: list
    """
    third_loc_id = request.GET.get('previous_loc')
    fourth_loc = Fourth_location.objects.filter(previous_loc_id=third_loc_id).order_by('name')
    return render(request, 'hr/fourth_loc_dropdown_list_options.html', {'fourth_loc': fourth_loc})


def load_fifth_location(request):
    """
    Method used in Location Management to get fifth location based on fourth location choice
    :rtype: list
    """
    fourth_loc_id = request.GET.get('previous_loc')
    fifth_loc = Fifth_location.objects.filter(previous_loc_id=fourth_loc_id).order_by('name')
    return render(request, 'hr/fifth_loc_dropdown_list_options.html', {'fifth_loc': fifth_loc})


def load_sixth_location(request):
    """
    Method used in Location Management to get sixth location based on fifth location choice
    :rtype: list
    """
    fifth_loc_id = request.GET.get('previous_loc')
    sixth_loc = Sixth_location.objects.filter(previous_loc_id=fifth_loc_id).order_by('name')
    return render(request, 'hr/sixth_loc_dropdown_list_options.html', {'sixth_loc': sixth_loc})


def load_seventh_location(request):
    """
    Method used in Location Management to get seventh location based on sixth location choice
    :rtype: list
    """
    sixth_loc_id = request.GET.get('previous_loc')
    seventh_loc = Seventh_location.objects.filter(previous_loc_id=sixth_loc_id).order_by('name')
    return render(request, 'hr/seventh_loc_dropdown_list_options.html', {'seventh_loc': seventh_loc})


def load_eighth_location(request):
    """
    Method used in Location Management to get eighth location based on seventh location choice
    :rtype: list
    """
    seventh_loc_id = request.GET.get('previous_loc')
    eighth_loc = Eighth_location.objects.filter(previous_loc_id=seventh_loc_id).order_by('name')
    return render(request, 'hr/eighth_loc_dropdown_list_options.html', {'eighth_loc': eighth_loc})


# Export database to csv
# Generate CSV File Instance List
def database_csv(request):
    """
    Method used in Report Management to get the list of registered items (Consumable + Assemblies + Piece Instances)
    on csv format
    :rtype: list
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=database.csv'
    location = ''

    # Create a csv writer
    writer = csv.writer(response)

    myinstancelist = []
    myassemblylist = []
    for i in PieceInstance.objects.all():
        myinstancelist.append(i)
    for i in Kit.objects.all():
        myassemblylist.append(i)
    mylist = (myinstancelist + myassemblylist)

    # Add column headings to the csv file
    writer.writerow(['Piece/Assembly', 'Piece model', 'Manufacturer', 'Manufacturer Part Number', 'Manufacturer Serial Number',
                       'Website',
                     'Description', 'Documentation', 'Calibration Recurrence', 'Type', 'Characteristic', 'Owner',
                     'Restriction', 'RSPL', 'Obsolete', 'Assembly Name','Group Assembly Name', 'CAE Part Number', 'CAE Serial Number', 'OEM',
                     'OEM Part Number', 'Provider Serial Number',
                     'First Location', 'Second Location', 'Third Location', 'Fourth Location', 'Fifth Location',
                     'Sixth Location', 'Seventh Location', 'Eighth Location',
                     'Status', 'Date created',
                     'Next calibration date', 'End of life', 'End of guarantee'])

    # Loop Through instance and output
    for item in mylist:
        # We check if item has group_assembly attribute hence it is an Assembly
        if hasattr(item, 'group_assembly'):
            writer.writerow(
                [item.name, None,  item.group_assembly.manufacturer, item.group_assembly.manufacturer_part_number,
                 item.manufacturer_serialnumber, None, item.description,
                 None, None,
                 None, None, None,
                 None, None, None, item.name, item.group_assembly.name, item.group_assembly.kit_partnumber, item.kit_serialnumber,
                 item.group_assembly.provider, item.group_assembly.provider_part_number, item.provider_serialnumber,
                 item.first_location, item.second_location, item.third_location, item.fourth_location,
                 item.fifth_location, item.sixth_location, item.seventh_location, item.eighth_location,
                 item.kit_status, item.date_created, None,
                 None, None, None])
        else:
            if item.is_rspl:
                rspl = 'RSPL'
            elif not item.is_rspl:
                rspl = 'Not RSPL'
            if item.piece.is_obsolete:
                obsolete = 'YES'
            elif not item.piece.is_obsolete:
                obsolete = 'NO'
            try:
                kit = Kit.objects.get(
                    Q(piece_kit_1=item) | Q(piece_kit_2=item) | Q(piece_kit_3=item) | Q(piece_kit_4=item)
                    | Q(piece_kit_5=item) | Q(piece_kit_6=item) | Q(piece_kit_7=item) | Q(piece_kit_8=item)
                    | Q(piece_kit_9=item) | Q(piece_kit_10=item) | Q(piece_kit_11=item) | Q(piece_kit_12=item)
                    | Q(piece_kit_13=item) | Q(piece_kit_14=item) | Q(piece_kit_15=item))
                groupassembly = kit.group_assembly.name
            except:
                kit = None
                groupassembly = None

            writer.writerow([item.piece.name, item.piece.piece_model, item.piece.manufacturer, item.piece.manufacturer_part_number,
                            item.manufacturer_serialnumber, item.piece.website, item.piece.description,
                            item.piece.documentation, item.piece.calibration_recurrence,
                            item.piece.item_type, item.piece.item_characteristic, item.owner,
                            item.restriction, rspl, obsolete, kit, groupassembly,  item.piece.cae_part_number, item.serial_number,
                            item.piece.provider, item.piece.provider_part_number,  item.provider_serialnumber,
                            item.first_location, item.second_location, item.third_location, item.fourth_location,
                            item.fifth_location, item.sixth_location, item.seventh_location, item.eighth_location,
                            item.status, item.date_created,
                            item.date_calibration, item.date_end_of_life, item.date_guarantee])
    return response


# Generate reports
# Shipped/Received
def shipped_received_display(request):
    """
    Method used in Report Management to get the list of Piece instance that have been 'Shipped' or 'Received' between
    two specific dates
    :rtype: list
    """
    if request.method == "POST":
        date1 = request.POST.get('sr_start_date')
        date2 = request.POST.get('sr_end_date')
        start_date = pd.to_datetime(date1).date()
        end_date = pd.to_datetime(date2).date()
        history = []
        instances = PieceInstance.objects.all()

        for instance in instances:
            myhistory = instance.history.all()
            for h in myhistory:
                if start_date <= h.history_date.date() <= end_date:
                    if h.status == 'Shipped' or h.status == 'Received':
                        h.history_date = h.history_date.date()
                        history.append(h)
        context = {'history': history, 'start_date': start_date, 'end_date': end_date}
    return render(request, 'inventory/reports/shipped_received_report.html', context)


def shipped_received_csv(request):
    """
    Method used in Report Management to get the list of Piece instance that have been 'Shipped' or 'Received' between
    two specific dates on csv format
    :rtype: list
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=shipped_received.csv'
    location = ''
    if request.method == "POST":
        date1 = request.POST.get('sr_start_date')
        date2 = request.POST.get('sr_end_date')
        start_date = pd.to_datetime(date1).date()
        end_date = pd.to_datetime(date2).date()
        # Create a csv writer
        writer = csv.writer(response)
        history = []
        instances = PieceInstance.objects.all()

        for instance in instances:
            myhistory = instance.history.all()
            for h in myhistory:
                if start_date <= h.history_date.date() <= end_date:
                    if h.status == 'Shipped' or h.status == 'Received':
                        h.history_date = h.history_date.date()
                        history.append(h)
        #list of all the history of the objects

        # Add column headings to the csv file
        writer.writerow(['Date', 'Status', 'Piece/Assembly', 'CAE Part Number', 'CAE Serial Number', 'Documentation',
                        'Description', 'Comment'])
        # Loop Through instance and output
        for item in history:
            writer.writerow([item.history_date, item.status, item.piece, item.piece.cae_part_number, item.serial_number,
                         item.piece.documentation, item.piece.description, item.update_comment])
    return response


# Reparation
def reparation_record_display(request):
    """
    Method used in Report Management to get the list of Piece instance that have been 'in Repair' between two specific
    dates
    :rtype: list
    """
    if request.method == "POST":
        date1 = request.POST.get('rep_start_date')
        date2 = request.POST.get('rep_end_date')
        start_date = pd.to_datetime(date1).date()
        end_date = pd.to_datetime(date2).date()
        instances = PieceInstance.objects.all()
        history = []
        for instance in instances:
            if instance.time_spent_in_r_instance():
                myhistory = instance.history.all()
                # We check that the history is between the start and end date
                for h in myhistory:
                    if start_date <= h.history_date.date() <= end_date and h.status == 'In Repair':
                        h.history_date = h.history_date.date()
                        history.append(h)
        context = {'history': history, 'start_date': start_date, 'end_date': end_date}
    return render(request, 'inventory/reports/reparation_record_report.html', context)


def reparation_record_csv(request):
    """
    Method used in Report Management to get the list of Piece instance that have been 'in Repair' between two specific
    dates on csv format
    :rtype: list
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=reparation_report.csv'
    location = ''
    if request.method == "POST":
        date1 = request.POST.get('rep_start_date')
        date2 = request.POST.get('rep_end_date')
        start_date = pd.to_datetime(date1).date()
        end_date = pd.to_datetime(date2).date()
        # Create a csv writer
        writer = csv.writer(response)
        history = []
        instances = PieceInstance.objects.all()
        for instance in instances:
            if instance.time_spent_in_r_instance():
                myhistory = instance.history.all()
                # We check that the history is between the start and end date
                for h in myhistory:
                    if start_date <= h.history_date.date() <= end_date and h.status == 'In Repair':
                        history.append(h)
        #list of all the history of the objects

        # Add column headings to the csv file
        writer.writerow(['Instance', 'CAE Part Number', 'CAE Serial Number', 'Documentation',
                     'Description', 'Date in Repair'])
        # Loop Through instance and output
        for item in history:
            writer.writerow([item.piece, item.piece.cae_part_number, item.serial_number, item.piece.documentation,
                            item.piece.description, item.history_date.date()])
    return response


# Movements
def movement_record_display(request):
    """
    Method used in Report Management to get the list of Movements between two specific dates
    :rtype: list
    """
    if request.method == "POST":
        date1 = request.POST.get('mov_start_date')
        date2 = request.POST.get('mov_end_date')
        start_date = pd.to_datetime(date1).date()
        end_date = pd.to_datetime(date2).date()
        history = []
        movements = MovementExchange.objects.all()
        for movement in movements:
            myhistory = movement.history.all()
            for h in myhistory:
                if start_date <= h.history_date.date() <= end_date:
                    h.history_date = h.history_date.date()
                    history.append(h)
        # list of all the history of the objects
        context = {'history': history, 'start_date': start_date, 'end_date': end_date}
    return render(request, 'inventory/reports/movement_record_report.html', context)


def movement_record_csv(request):
    """
    Method used in Report Management to get the list of Movements between two specific dates on csv format
    :rtype: list
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=movement_report.csv'
    location = ''
    if request.method == "POST":
        date1 = request.POST.get('mov_start_date')
        date2 = request.POST.get('mov_end_date')
        start_date = pd.to_datetime(date1).date()
        end_date = pd.to_datetime(date2).date()

        # Create a csv writer
        writer = csv.writer(response)
        history = []
        movements = MovementExchange.objects.all()

        for movement in movements:
            myhistory = movement.history.all()
            for h in myhistory:
                if start_date <= h.history_date.date() <= end_date:
                    history.append(h)
        #list of all the history of the objects

        # Add column headings to the csv file
        writer.writerow(['Date', 'Reference Number',
                        'Piece Exchanged', 'PE CAE Part Number', 'PE CAE Serial Number', 'PE Comment',
                        'Replacing Piece', 'RP CAE Part Number', 'RP CAE Serial Number', 'RP Comment',
                        ])
        # Loop Through instance and output
        for item in history:
            writer.writerow([item.history_date.date() , item.reference_number,
                            item.piece_1, item.piece_1.cae_part_number, item.item_1.serial_number,
                            item.update_comment_item1,
                            item.piece_2, item.piece_2.cae_part_number, item.item_2.serial_number,
                            item.update_comment_item2,
                            ])
    return response


# Generate Low Stock record
def low_stock_record_display(request):
    """
    Method used in Report Management to get the list of items in Low Stock
    :rtype: list
    """
    myconsumablelist = []
    for item in Consumable.objects.all():
        if item.is_low_stock():
            myconsumablelist.append(item)
        # list of all the history of the objects
        context = {'myconsumablelist': myconsumablelist}
    return render(request, 'inventory/reports/low_stock_record_report.html', context)


def low_stock_record_csv(request):
    """
    Method used in Report Management to get the list of items in Low Stock on csv format
    :rtype: list
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=low_stock_database.csv'
    location = ''

    # Create a csv writer
    writer = csv.writer(response)

    myconsumablelist = []
    for item in Consumable.objects.all():
        if item.is_low_stock():
            myconsumablelist.append(item)

    # Add column headings to the csv file
    writer.writerow(['Name', 'CAE PArt Number', 'CAE Serial Number',
                     'Manufacturer', 'Manufacturer Part Number', 'Manufacturer Serial Number',
                     'Provider', 'Provider Part Number', 'Provider Serial Number',
                     'Website',
                     'Description', 'Documentation', 'Type', 'Characteristic', 'RSPL',
                     'Quantity', 'Threshold',
                     'First Location', 'Second Location', 'Third Location', 'Fourth Location', 'Fifth Location',
                     'Sixth Location', 'Seventh Location', 'Eighth Location',
                     'Status', 'Date created', 'Owner', 'Restriction'])

    # Loop Through instance and output
    for item in myconsumablelist:
        # We check if item has group_assembly attribute hence it is an Assembly
        if item.is_rspl:
            rspl = 'RSPL'
        elif not item.is_rspl:
            rspl = 'Not RSPL'
        writer.writerow([item.name, item.cae_part_number, item.serial_number,
                        item.manufacturer, item.manufacturer_part_number, item.manufacturer_serialnumber,
                        item.provider, item.provider_part_number, item.provider_serialnumber,
                        item.website,
                        item.description, item.documentation, item.item_type, item.item_characteristic, rspl,
                        item.quantity, item.low_stock_value,
                        item.first_location, item.second_location, item.third_location, item.fourth_location,
                        item.fifth_location, item.sixth_location, item.seventh_location, item.eighth_location,
                        item.status, item.date_created, item.owner, item.restriction])
    return response


class ConsumableCreate(CreateView):
    """
    View to display ConsumableForm
    """
    template_name = 'inventory/consumable/create_consumable.html'
    model = Consumable
    form_class = ConsumableForm

    def get(self, request, *args, **kwargs):
        """
        A dictionary-like object containing all given HTTP GET parameters
        :rtype: ConsumableForm
        """
        self.object = None
        form_class = self.get_form_class()
        form = ConsumableForm()
        context = {
            'form': form,
        }
        return render(request, 'inventory/consumable/create_consumable.html', context)

    def post(self, request, *args, **kwargs):
        """
        A dictionary-like object containing all given HTTP POST parameters,
        providing that the request contains form data
        :rtype: ConsumableForm
        """
        self.object = None
        form_class = self.get_form_class()
        form = ConsumableForm(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Override of form_valid method
        :rtype: ConsumableForm
        """
        self.object = form.save()
        # instance_form.instance = self.object
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Override of form_invalid method
        :rtype: ConsumableForm
        """
        return self.render_to_response(
            self.get_context_data(form=form))


# Display specific consumable
def show_consumable(request, primary_key):
    """
    Function to display Consumable detail
    :rtype: Consumable
    """
    consumable = Consumable.objects.get(pk=primary_key)
    context = {'consumable': consumable}
    return render(request, 'inventory/consumable/consumable_detail.html', context)


def consumable_list(request):
    """
    Function to get all Consumables ordered by name
    :rtype: list
    """
    consumable_list = Consumable.objects.all().order_by('name')
    return render(request, 'inventory/consumable/consumable_list.html', {'consumable_list': consumable_list})


# Update a consumable
def update_consumable(request, consumable_id):
    """
    Function to update Consumable
    :rtype: ConsumableForm, Consumable
    """
    consumable = Consumable.objects.get(pk=consumable_id)
    consumable.update_comment = ''
    if request.method == "POST":
        form = ConsumableForm(request.POST, request.FILES, instance=consumable)
        if form.is_valid():
            form.save()
            return redirect(consumable.get_absolute_url())
    else:
        form = ConsumableForm(instance=consumable)
    context = {'consumable': consumable, 'form': form}
    return render(request, 'inventory/consumable/update_consumable.html', context)


# clone a consumable
def clone_consumable(request, consumable_id):
    """
    Function to clone Consumable
    :rtype: ConsumableForm, Consumable
    """
    consumable = Consumable.objects.get(pk=consumable_id)
    consumable.pk=None
    consumable.update_comment = ''
    if request.method == "POST":
        form = ConsumableForm(request.POST, request.FILES, instance=consumable)
        if form.is_valid():
            form.save()
            return redirect(consumable.get_absolute_url())
    else:
        form = ConsumableForm(instance=consumable)
    context = {'consumable': consumable, 'form': form}
    return render(request, 'inventory/consumable/clone_consumable.html', context)


# Piece Creation
class PieceCreate(CreateView):
    """
    View to display PieceForm
    """
    template_name = 'inventory/piece/create_piece.html'
    model = Piece
    form_class = PieceForm

    def get(self, request, *args, **kwargs):
        """
        A dictionary-like object containing all given HTTP GET parameters
        :rtype: PieceForm
        """
        self.object = None
        form_class = self.get_form_class()
        form = PieceForm()
        context = {
            'form': form,
        }
        return render(request, 'inventory/piece/create_piece.html', context)

    def post(self, request, *args, **kwargs):
        """
        A dictionary-like object containing all given HTTP POST parameters,
        providing that the request contains form data
        :rtype: PieceForm
        """
        # if our ajax is calling so we have to take action
        # because this is not the form submission
        if request.is_ajax():
            cp = request.POST.copy()  # because we couldn't change fields values directly in request.POST
            value = int(cp['wtd'])  # figure out if the process is addition or deletion
            prefix = "instance_reverse"
            cp[f'{prefix}-TOTAL_FORMS'] = int(
                cp[f'{prefix}-TOTAL_FORMS']) + value
            formset = PieceInstancePieceFormSet(cp)  # catch any data which were in the previous formsets and deliver to-
            # the new formsets again -> if the process is addition!
            return render(request, 'inventory/formset.html', {'formset': formset})

        self.object = None
        form_class = self.get_form_class()
        form = PieceForm(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, request):
        """
        Override of form_valid method
        :rtype: PieceForm
        """
        # We check no piece with same part number already exist
        pieces = Piece.objects.all()
        self.object = form.save(commit=False)
        for piece in pieces:
            # Protection in case a Piece with given part number already exist
            if self.object.cae_part_number == piece.cae_part_number:
                # We populate message and return the form with the message display to inform User
                messages.success(request, 'A piece with this part number already exist')
                return self.render_to_response(self.get_context_data(form=form))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Override of form_invalid method
        :rtype: PieceForm
        """
        return self.render_to_response(
            self.get_context_data(form=form))


# Display a list of all the Pieces in the inventory
class PieceListView(ListView):
    """
    List of Pieces
    """
    model = Piece
    paginate_by = 10
    template_name = 'inventory/piece/piece_list.html'  # Template location

    def get_context_data(self, **kwargs):
        """
        Returns context data for displaying the list of objects.
        :rtype: list
        """
        # Call the base implementation first to get the context
        context = super(PieceListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['piece'] = Piece.objects.all().order_by('-id')
        return context


# Display a specific Piece
def show_piece(request, primary_key):
    """
    Function to display Piece detail, its Equivalences and PieceInstances that are part of it
    :rtype: Piece, Equivalence, PieceInstance
    """
    piece = Piece.objects.get(pk=primary_key)
    piece_instance = PieceInstance.objects.all().order_by('status')
    # Instance management
    instance_installed = PieceInstance.objects.filter(status='Installed', piece=piece).count()
    instance_in_stock = PieceInstance.objects.filter(status='In Stock', piece=piece).count()
    instance_discarded = PieceInstance.objects.filter(status='Discarded', piece=piece).count()
    instance_in_reparation = PieceInstance.objects.filter(status='In Repair', piece=piece).count()
    # Equivalence management
    equivalences = Equivalence.objects.all()
    my_eq_list = []
    # First we create a list of all the equivalences in which our piece is
    for equivalence in equivalences:
        piece_eq_list = [equivalence.pieceeq_1, equivalence.pieceeq_2, equivalence.pieceeq_3, equivalence.pieceeq_4,
                         equivalence.pieceeq_5, equivalence.pieceeq_6, equivalence.pieceeq_7, equivalence.pieceeq_8,
                         equivalence.pieceeq_9, equivalence.pieceeq_10, equivalence.pieceeq_11, equivalence.pieceeq_12,
                         equivalence.pieceeq_13, equivalence.pieceeq_14, equivalence.pieceeq_15]
        for piece_eq in piece_eq_list:
            if piece_eq == piece:
                for my_piece in piece_eq_list:
                    # We make sure the equivalent piece is not our piece and not empty
                    if my_piece is not None and my_piece != piece:
                        my_eq_list.append(my_piece)
    # my_eq_list contains all the pieces that are equivalent to our piece
    # We now want to remove any duplicates therefore we are going to create a dictionary using the list items as keys.
    # This will automatically remove any duplicates because dictionaries cannot have duplicates
    my_eq_list = list(dict.fromkeys(my_eq_list))
    context = {'piece': piece, 'piece_instance': piece_instance, 'instance_installed': instance_installed,
               'instance_in_stock': instance_in_stock, 'instance_discarded': instance_discarded,
               'instance_in_reparation': instance_in_reparation, 'my_eq_list': my_eq_list}
    return render(request, 'inventory/piece/piece_detail.html', context)


# Update a piece
def update_piece(request, piece_id):
    """
    Function to update Piece
    :rtype: PieceForm, Piece
    """
    piece = Piece.objects.get(pk=piece_id)
    piece.update_comment = ''
    if request.method == "POST":
        form = PieceForm(request.POST, request.FILES, instance=piece)
        if form.is_valid():
            form.save()
            return redirect(piece.get_absolute_url())
    else:
        form = PieceForm(instance=piece)
    context = {'piece': piece, 'form': form}
    return render(request, 'inventory/piece/update_piece.html', context)


# clone a piece
def clone_piece(request, piece_id):
    """
    Function to clone Piece
    :rtype: PieceForm, Piece
    """
    pieces = Piece.objects.all()
    piece = Piece.objects.get(pk=piece_id)
    piece.pk = None
    piece.update_comment = ''
    if request.method == "POST":
        form = PieceForm(request.POST, request.FILES, instance=piece)
        context = {'piece': piece, 'form': form}
        if form.is_valid():
            object = form.save(commit=False)
            for mypiece in pieces:
                if object.cae_part_number == mypiece.cae_part_number:
                    messages.success(request, 'A piece with this part number already exist')
                    return render(request, 'inventory/piece/clone_piece.html', context)
            object.save()
            return redirect(piece.get_absolute_url())
    else:
        form = PieceForm(instance=piece)
    context = {'piece': piece, 'form': form}
    return render(request, 'inventory/piece/clone_piece.html', context)


# Instance creation
class PieceInstanceCreate(CreateView):
    """
    View to display PieceInstanceForm
    """
    template_name = 'inventory/instances/create_instance_piece.html'
    model = PieceInstance
    form_class = PieceInstanceForm

    def get(self, request, *args, **kwargs):
        """
        A dictionary-like object containing all given HTTP GET parameters
        :rtype: PieceInstanceForm
        """
        self.object = None
        form_class = self.get_form_class()
        form = PieceInstanceForm()
        pieces = Piece.objects.all()
        context = {
            'form': form, 'pieces': pieces,
        }
        return render(request, 'inventory/instances/create_instance_piece.html', context)

    def post(self, request, *args, **kwargs):
        """
        A dictionary-like object containing all given HTTP POST parameters,
        providing that the request contains form data
        :rtype: PieceInstanceForm
        """
        # if our ajax is calling so we have to take action
        # because this is not the form submission
        if request.is_ajax():
            cp = request.POST.copy()  # because we couldn't change fields values directly in request.POST
            value = int(cp['wtd'])  # figure out if the process is addition or deletion
            prefix = "instance_reverse"
            cp[f'{prefix}-TOTAL_FORMS'] = int(
                cp[f'{prefix}-TOTAL_FORMS']) + value
            formset = PieceInstancePieceFormSet(cp)  # catch any data which were in the previous formsets and deliver to-
            # the new formsets again -> if the process is addition!
            return render(request, 'inventory/formset.html', {'formset': formset})
        self.object = None
        form_class = self.get_form_class()
        form = PieceInstanceForm(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def form_valid(self, request, form):
        """
        Override of form_valid method
        :rtype: PieceInstanceForm
        """
        piece_instance = PieceInstance.objects.all()
        self.object = form.save(commit=False)
        for instance in piece_instance:
            if self.object.piece == instance.piece:
                if self.object.serial_number == instance.serial_number:
                    messages.success(request, 'An instance with this serial number already exist')
                    return self.render_to_response(self.get_context_data(form=form))
        self.object.save()
        # instance_form.instance = self.object
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Override of form_invalid method
        :rtype: PieceInstanceForm
        """
        print('invalid')
        return self.render_to_response(
            self.get_context_data(form=form))


# Add instance from Piece page
def add_instance(request, piece_id):
    """
    Function to add Piece Instance directly from Piece detail page
    :rtype: PieceInstanceForm
    """
    piece = Piece.objects.get(pk=piece_id)
    if request.method == "POST":
        if request.is_ajax():
            cp = request.POST.copy()  # because we couldn't change fields values directly in request.POST
            value = int(cp['wtd'])  # figure out if the process is addition or deletion
            prefix = "instance_reverse"
            cp[f'{prefix}-TOTAL_FORMS'] = int(
                cp[f'{prefix}-TOTAL_FORMS']) + value
            formset = PieceInstancePieceFormSet(cp)  # catch any data which were in the previous formsets and deliver to-
            # the new formsets again -> if the process is addition!
            return render(request, 'inventory/formset.html', {'formset': formset})
        form = PieceInstanceForm(request.POST, request.FILES, {'piece': piece})
        context = {'form': form}
        if form.is_valid():
            piece_instance = PieceInstance.objects.all()
            object = form.save(commit=False)
            for instance in piece_instance:
                if object.piece == instance.piece:
                    if object.serial_number == instance.serial_number:
                        messages.success(request, 'An instance with this serial number already exist')
                        return render(request, 'inventory/instances/add_pieceinstance.html', context)
            object.save()
            return redirect(object.get_absolute_url())
    else:
        form = PieceInstanceForm({'piece': piece})
    context = {'form': form}
    return render(request, 'inventory/instances/add_pieceinstance.html', context)


def all_piece_instance(request):
    """
    Function to get all PieceInstances
    :rtype: list
    """
    piece_instance_list = PieceInstance.objects.all().order_by('piece')
    return render(request, 'inventory/instances/piece_instance_list.html', {'piece_instance_list': piece_instance_list})


# Display specific instance information
def show_instance_form(request, primary_key):
    """
    Function to display PieceInstance detail and its Kit if it is part of one
    :rtype: PieceInstance, Kit
    """
    piece_instance = PieceInstance.objects.get(pk=primary_key)
    try:
        kit = Kit.objects.get(
            Q(piece_kit_1=piece_instance) | Q(piece_kit_2=piece_instance) | Q(piece_kit_3=piece_instance) | Q(piece_kit_4=piece_instance)
            | Q(piece_kit_5=piece_instance) | Q(piece_kit_6=piece_instance) | Q(piece_kit_7=piece_instance) | Q(piece_kit_8=piece_instance)
            | Q(piece_kit_9=piece_instance) | Q(piece_kit_10=piece_instance) | Q(piece_kit_11=piece_instance) | Q(piece_kit_12=piece_instance)
            | Q(piece_kit_13=piece_instance) | Q(piece_kit_14=piece_instance) | Q(piece_kit_15=piece_instance))
    except:
        kit = None
    context = {'piece_instance': piece_instance, 'kit': kit}
    return render(request, 'inventory/instances/piece_instance_detail.html', context)


# Display instances and assembly as list
def show_instance_assembly_list(request):
    """
    Function to get all PieceInstances and Assemblies
    :rtype: list
    """
    # We create 2 lists to regroup objects from pieceInstance and Kit
    myinstancelist=[]
    myassemblylist=[]
    myconsumablelist=[]
    for i in PieceInstance.objects.all():
        myinstancelist.append(i)
    for i in Kit.objects.all():
        myassemblylist.append(i)
    for i in Consumable.objects.all():
        myconsumablelist.append(i)
    # We assemble one list under one for display purpose
    mylist = (myinstancelist + myassemblylist + myconsumablelist)
    context = {'mylist': mylist}
    return render(request, 'inventory/general_list.html', context)


# Update an instance
def update_instance(request, instance_id):
    """
    Function to update PieceInstance
    :rtype: PieceInstanceForm, PieceInstance
    """
    piece_instance = PieceInstance.objects.get(pk=instance_id)
    piece_instance.date_update = datetime.date.today()
    piece_instance.update_comment = ''
    if request.method == "POST":
        form = PieceInstanceForm(request.POST, request.FILES, instance=piece_instance)
        if form.is_valid():
            form.save()
            return redirect(piece_instance.get_absolute_url())
    else:
        form = PieceInstanceForm(instance=piece_instance)
    context = {'piece_instance': piece_instance, 'form': form}
    return render(request, 'inventory/instances/update_piece_instance.html', context)


# clone an instance
def clone_instance(request, instance_id):
    """
    Function to clone PieceInstance
    :rtype: PieceInstanceForm, PieceInstance
    """
    instances = PieceInstance.objects.all()
    piece_instance = PieceInstance.objects.get(pk=instance_id)
    piece_instance.update_comment = ''
    if request.method == "POST":
        piece_instance.pk = None
        form = PieceInstanceForm(request.POST, request.FILES, instance=piece_instance)
        context = {'piece_instance': piece_instance, 'form': form}
        if form.is_valid():
            object = form.save(commit=False)
            for instance in instances:
                if object.serial_number == instance.serial_number:
                    messages.success(request, 'An Instance with this part number already exist')
                    return render(request, 'inventory/instances/clone_existing_piece.html', context)
            object.save()
            return redirect(piece_instance.get_absolute_url())
    else:
        form = PieceInstanceForm(instance=piece_instance)
    context = {'piece_instance': piece_instance, 'form': form}
    return render(request, 'inventory/instances/clone_existing_piece.html', context)


# Delete an instance
def delete_instance(request, instance_id):
    """
    Function to delete PieceInstance
    """
    piece_instance = PieceInstance.objects.get(pk=instance_id)
    piece_instance.delete()
    return redirect('piece-list')


# Search feature
# Specific to Consumable
def search_consumable_database(request):
    """
    Function to retrieve Consumables which have attributes fitting the searched term from the html page
    :rtype: list
    """
    if request.method == "POST":
        searched = request.POST['searched']
        if searched == 'RSPL' or searched == 'rspl':
            results = Consumable.objects.filter(is_rspl=True)
        else:
            results = Consumable.objects.filter(Q(name__contains=searched)
                                       | Q(manufacturer__contains=searched)
                                       | Q(manufacturer_part_number__contains=searched)
                                       | Q(cae_part_number__contains=searched)
                                       | Q(provider_part_number__contains=searched)
                                       | Q(provider__contains=searched)
                                       | Q(item_type__contains=searched)
                                       | Q(item_characteristic__contains=searched)
                                       | Q(item_characteristic__contains=searched)
                                       | Q(first_location__name__contains=searched)
                                       | Q(second_location__name__contains=searched)
                                       | Q(third_location__name__contains=searched)
                                       | Q(fourth_location__name__contains=searched)
                                       | Q(fifth_location__name__contains=searched)
                                       | Q(sixth_location__name__contains=searched)
                                       | Q(seventh_location__name__contains=searched)
                                       | Q(eighth_location__name__contains=searched)
                                       | Q(manufacturer_part_number__contains=searched)
                                       | Q(status__contains=searched)
                                       | Q(serial_number__contains=searched)
                                       | Q(manufacturer_serialnumber__contains=searched)
                                       | Q(owner__contains=searched)
                                       | Q(provider_serialnumber__contains=searched)
                                       )
        context = {'searched': searched, 'results': results}
        return render(request, 'inventory/search/search_consumable.html', context)
    else:
        return render(request, 'inventory/search/search_consumable.html', {})


# Specific to piece
def search_piece_database(request):
    """
    Function to retrieve Pieces which have attributes fitting the searched term from the html page
    :rtype: list
    """
    if request.method == "POST":
        searched = request.POST['searched']
        if searched == 'obsolete':
            results = Piece.objects.filter(is_obsolete=True)
        else:
            results = Piece.objects.filter(Q(piece_model__contains=searched)
                                       | Q(manufacturer__contains=searched)
                                       | Q(manufacturer_part_number__contains=searched)
                                       | Q(cae_part_number__contains=searched)
                                       | Q(provider_part_number__contains=searched)
                                       | Q(provider__contains=searched)
                                       | Q(item_type__contains=searched)
                                       )
        context = {'searched': searched, 'results': results}
        return render(request, 'inventory/search/search.html', context)
    else:
        return render(request, 'inventory/search/search.html', {})


# Specific to instances
def search_instance_database(request):
    """
    Function to retrieve PieceInstances which have attributes fitting the searched term from the html page
    :rtype: list
    """
    if request.method == "POST":
        searched = request.POST['searched']
        if searched == 'RSPL' or searched == 'rspl':
            results = PieceInstance.objects.filter(is_rspl=True)
        else:
            results = PieceInstance.objects.filter(Q(first_location__name__contains=searched)
                                                   | Q(second_location__name__contains=searched)
                                                   | Q(third_location__name__contains=searched)
                                                   | Q(fourth_location__name__contains=searched)
                                                   | Q(fifth_location__name__contains=searched)
                                                   | Q(sixth_location__name__contains=searched)
                                                   | Q(seventh_location__name__contains=searched)
                                                   | Q(eighth_location__name__contains=searched)
                                                   | Q(piece__manufacturer_part_number__contains=searched)
                                                   | Q(status__contains=searched)
                                                   | Q(serial_number__contains=searched)
                                                   | Q(manufacturer_serialnumber__contains=searched)
                                                   | Q(owner__contains=searched)
                                                   | Q(provider_serialnumber__contains=searched)
                                                   )
        context = {'searched': searched, 'results': results}
        return render(request, 'inventory/search/search_instance.html', context)
    else:
        return render(request, 'inventory/search/search_instance.html', {})


# Specific to Assemblies
# Specific to Group Assemblies
def search_groupassembly_database(request):
    """
    Function to retrieve GroupAssemblies which have attributes fitting the searched term from the html page
    :rtype: list
    """
    if request.method == "POST":
        searched = request.POST['searched']
        results = GroupAssembly.objects.filter(Q(name__contains=searched)
                                       | Q(kit_partnumber__contains=searched)
                                       | Q(update_comment__contains=searched)
                                       )
        context = {'searched': searched, 'results': results}
        return render(request, 'inventory/search/search_groupassembly.html', context)
    else:
        return render(request, 'inventory/search/search_groupassembly.html', {})


# Specific to Assemblies
def search_assembly_database(request):
    """
    Function to retrieve Assemblies which have attributes fitting the searched term from the html page
    :rtype: list
    """
    if request.method == "POST":
        searched = request.POST['searched']
        results = Kit.objects.filter(Q(group_assembly__name__contains=searched)
                                       | Q(group_assembly__kit_partnumber__contains=searched)
                                       | Q(group_assembly__update_comment__contains=searched)
                                       | Q(first_location__name__contains=searched)
                                       | Q(second_location__name__contains=searched)
                                       | Q(third_location__name__contains=searched)
                                       | Q(fourth_location__name__contains=searched)
                                       | Q(fifth_location__name__contains=searched)
                                       | Q(sixth_location__name__contains=searched)
                                       | Q(seventh_location__name__contains=searched)
                                       | Q(eighth_location__name__contains=searched)
                                       | Q(name__contains=searched)
                                       | Q(kit_status__contains=searched)
                                       | Q(kit_serialnumber__contains=searched)
                                       )
        context = {'searched': searched, 'results': results}
        return render(request, 'inventory/search/search_assembly.html', context)
    else:
        return render(request, 'inventory/search/search_assembly.html', {})


# Specific to General List
def search_general_database(request):
    """
    Function to retrieve PiecesInstances, Consumables and Assemblies which have attributes fitting the searched term
    from the html page
    :rtype: list
    """
    if request.method == "POST":
        searched = request.POST['searched']
        results_rspl = []
        results_instance = []
        results_assemblies = []
        results_consumable = []
        if searched == 'RSPL' or searched == 'rspl':
            for i in PieceInstance.objects.filter(is_rspl=True):
                print(i)
                results_rspl.append(i)
            for i in Consumable.objects.filter(is_rspl=True):
                print(i)
                results_rspl.append(i)
        else:
            for i in PieceInstance.objects.filter(Q(first_location__name__contains=searched)
                                                   | Q(second_location__name__contains=searched)
                                                   | Q(third_location__name__contains=searched)
                                                   | Q(fourth_location__name__contains=searched)
                                                   | Q(fifth_location__name__contains=searched)
                                                   | Q(sixth_location__name__contains=searched)
                                                   | Q(seventh_location__name__contains=searched)
                                                   | Q(eighth_location__name__contains=searched)
                                                   | Q(piece__manufacturer_part_number__contains=searched)
                                                   | Q(status__contains=searched)
                                                   | Q(serial_number__contains=searched)
                                                   | Q(manufacturer_serialnumber__contains=searched)
                                                   | Q(owner__contains=searched)
                                                   | Q(provider_serialnumber__contains=searched)
                                                   | Q(piece__piece_model__contains=searched)
                                                   | Q(piece__manufacturer__contains=searched)
                                                   | Q(piece__manufacturer_part_number__contains=searched)
                                                   | Q(piece__cae_part_number__contains=searched)
                                                   | Q(piece__provider_part_number__contains=searched)
                                                   | Q(piece__provider__contains=searched)
                                                   | Q(piece__item_type__contains=searched)
                                                   | Q(piece__item_characteristic__contains=searched)
                                                   | Q(piece__name__contains=searched)
                                                   ):
                results_instance.append(i)
            for i in Kit.objects.filter(Q(group_assembly__name__contains=searched)
                                                    | Q(group_assembly__kit_partnumber__contains=searched)
                                                    | Q(group_assembly__update_comment__contains=searched)
                                                    | Q(first_location__name__contains=searched)
                                                    | Q(second_location__name__contains=searched)
                                                    | Q(third_location__name__contains=searched)
                                                    | Q(fourth_location__name__contains=searched)
                                                    | Q(fifth_location__name__contains=searched)
                                                    | Q(sixth_location__name__contains=searched)
                                                    | Q(seventh_location__name__contains=searched)
                                                    | Q(eighth_location__name__contains=searched)
                                                    | Q(name__contains=searched)
                                                    | Q(kit_status__contains=searched)
                                                    | Q(kit_serialnumber__contains=searched)
                                                    ):
                results_assemblies.append(i)
            for i in Consumable.objects.filter(Q(name__contains=searched)
                                                    | Q(piece_model__contains=searched)
                                                    | Q(cae_part_number__contains=searched)
                                                    | Q(serial_number__contains=searched)
                                                    | Q(manufacturer__contains=searched)
                                                    | Q(manufacturer_part_number__contains=searched)
                                                    | Q(manufacturer_serialnumber__contains=searched)
                                                    | Q(provider__contains=searched)
                                                    | Q(provider_part_number__contains=searched)
                                                    | Q(provider_serialnumber__contains=searched)
                                                    | Q(item_type__contains=searched)
                                                    | Q(item_characteristic__contains=searched)
                                                    | Q(update_comment__contains=searched)
                                                    | Q(status__contains=searched)
                                                    | Q(condition__contains=searched)
                                                    | Q(restriction__contains=searched)
                                                    | Q(first_location__name__contains=searched)
                                                    | Q(second_location__name__contains=searched)
                                                    | Q(third_location__name__contains=searched)
                                                    | Q(fourth_location__name__contains=searched)
                                                    | Q(fifth_location__name__contains=searched)
                                                    | Q(sixth_location__name__contains=searched)
                                                    | Q(seventh_location__name__contains=searched)
                                                    | Q(eighth_location__name__contains=searched)
                                                    | Q(owner__contains=searched)
                                                    ):
                results_consumable.append(i)
        results = (results_consumable + results_assemblies + results_instance + results_rspl)
        context = {'searched': searched, 'results': results}
        return render(request, 'inventory/search/search_general.html', context)
    else:
        return render(request, 'inventory/search/search_general.html', {})


# Assembly Management Section
# Create Group Assembly
class GroupAssemblyCreate(CreateView):
    """
    View to display GroupAssemblyForm
    """
    template_name = 'inventory/group_assembly/create_groupassembly.html'
    model = GroupAssembly
    form_class = GroupAssemblyForm

    def get(self, request, *args, **kwargs):
        """
        A dictionary-like object containing all given HTTP GET parameters
        :rtype: GroupAssemblyForm
        """
        self.object = None
        form_class = self.get_form_class()
        form = GroupAssemblyForm()
        context = {
            'form': form,
        }
        return render(request, 'inventory/group_assembly/create_groupassembly.html', context)

    def post(self, request, *args, **kwargs):
        """
        A dictionary-like object containing all given HTTP POST parameters,
        providing that the request contains form data
        :rtype: GroupAssemblyForm
        """
        # if our ajax is calling so we have to take action
        # because this is not the form submission
        if request.is_ajax():
            cp = request.POST.copy()  # because we couldn't change fields values directly in request.POST
            value = int(cp['wtd'])  # figure out if the process is addition or deletion
            prefix = "instance_reverse"
            cp[f'{prefix}-TOTAL_FORMS'] = int(
                cp[f'{prefix}-TOTAL_FORMS']) + value
            formset = KitGroupAssemblyFormSet(cp)  # catch any data which were in the previous formsets and deliver to-
            # the new formsets again -> if the process is addition!
            return render(request, 'inventory/formset.html', {'formset': formset})

        self.object = None
        form_class = self.get_form_class()
        form = GroupAssemblyForm(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Override of form_valid method
        :rtype: GroupAssemblyForm
        """
        self.object = form.save()
        # instance_form.instance = self.object
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Override of form_invalid method
        :rtype: GroupAssemblyForm
        """
        return self.render_to_response(
            self.get_context_data(form=form))


# Display a list of all the Pieces in the inventory
class GroupAssemblyListView(ListView):
    """
    List of GroupAssemblies
    """
    model = GroupAssembly
    paginate_by = 10
    template_name = 'inventory/group_assembly/groupassembly_list.html'  # Template location

    def get_context_data(self, **kwargs):
        """
        Returns context data for displaying the list of objects.
        :rtype: list
        """
        # Call the base implementation first to get the context
        context = super(GroupAssemblyListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['groupassembly'] = GroupAssembly.objects.all().order_by('-id')
        return context


# Display a specific Group Assembly
def show_groupassembly(request, primary_key):
    """
    Function to display GroupAssembly detail and Kits that are part of it
    :rtype: GroupAssembly, Kit
    """
    groupassembly = GroupAssembly.objects.get(pk=primary_key)
    kit = Kit.objects.all().order_by('name')
    context = {'groupassembly': groupassembly, 'kit': kit}
    return render(request, 'inventory/group_assembly/groupassembly_detail.html', context)


# Create new assembly
class KitCreate(CreateView):
    """
    View to display KitForm
    """
    template_name = 'inventory/assembly/kit_form.html'
    model = Kit
    form_class = KitForm

    def form_valid(self, form):
        """
        Override of form_valid method
        :rtype: KitForm
        """
        instances = PieceInstance.objects.all()
        kit = form.save(commit=False)
        kit.save()
        piece_instance = [kit.piece_kit_1, kit.piece_kit_2, kit.piece_kit_3, kit.piece_kit_4, kit.piece_kit_5,
                          kit.piece_kit_6, kit.piece_kit_7, kit.piece_kit_8, kit.piece_kit_9, kit.piece_kit_10,
                          kit.piece_kit_11, kit.piece_kit_12, kit.piece_kit_13, kit.piece_kit_14,
                          kit.piece_kit_15]
        for item in piece_instance:
            if item is not None:
                for instance in instances:
                    if instance.serial_number == item.serial_number:
                        instance.update_comment = kit.update_comment
                        instance.first_location = kit.first_location
                        instance.second_location = kit.second_location
                        instance.third_location = kit.third_location
                        instance.fourth_location = kit.fourth_location
                        instance.fifth_location = kit.fifth_location
                        instance.sixth_location = kit.sixth_location
                        instance.seventh_location = kit.seventh_location
                        instance.eighth_location = kit.eighth_location
                        instance.status = kit.kit_status
                        instance.save()
        return redirect(kit.get_absolute_url())


# Update an assembly
def update_kit(request, kit_id):
    """
    Function to update Kit
    :rtype: KitForm, Kit
    """
    kit = Kit.objects.get(pk=kit_id)
    kit.date_update = timezone.now()
    kit.update_comment = ''
    instances = PieceInstance.objects.all()
    if request.method == "POST":
        form = KitForm(request.POST or None, instance=kit)
        if form.is_valid():
            parent = form.save(commit=False)
            parent.save()
            piece_instance = [kit.piece_kit_1, kit.piece_kit_2, kit.piece_kit_3, kit.piece_kit_4, kit.piece_kit_5,
                              kit.piece_kit_6, kit.piece_kit_7, kit.piece_kit_8, kit.piece_kit_9, kit.piece_kit_10,
                              kit.piece_kit_11, kit.piece_kit_12, kit.piece_kit_13, kit.piece_kit_14, kit.piece_kit_15]
            for item in piece_instance:
                if item is not None:
                    for instance in instances:
                        if instance == item:
                            instance.update_comment = kit.update_comment
                            instance.first_location = kit.first_location
                            instance.second_location = kit.second_location
                            instance.third_location = kit.third_location
                            instance.fourth_location = kit.fourth_location
                            instance.fifth_location = kit.fifth_location
                            instance.sixth_location = kit.sixth_location
                            instance.seventh_location = kit.seventh_location
                            instance.eighth_location = kit.eighth_location
                            instance.status = kit.kit_status
                            instance.save()
            return redirect(kit.get_absolute_url())
    else:
        form = KitForm(instance=kit)
    context = {
        'kit': kit,
        'form': form,
    }
    return render(request, 'inventory/assembly/kit_update.html', context)


def clone_kit(request, kit_id):
    """
    Function to clone Kit
    :rtype: KitForm, Kit
    """
    assemblies = Kit.objects.all()
    kit = Kit.objects.get(pk=kit_id)
    kit.date_update = timezone.now()
    kit.update_comment = ''
    kit.piece_kit_1 = None
    kit.piece_kit_2 = None
    kit.piece_kit_3 = None
    kit.piece_kit_4 = None
    kit.piece_kit_5 = None
    kit.piece_kit_6 = None
    kit.piece_kit_7 = None
    kit.piece_kit_8 = None
    kit.piece_kit_9 = None
    kit.piece_kit_10 = None
    kit.piece_kit_11 = None
    kit.piece_kit_12 = None
    kit.piece_kit_13 = None
    kit.piece_kit_14 = None
    kit.piece_kit_15 = None
    instances = PieceInstance.objects.all()
    if request.method == "POST":
        form = KitForm(request.POST or None, instance=kit)
        kit.pk = None
        context = {'kit': kit, 'form': form}
        if form.is_valid():
            parent = form.save(commit=False)
            for assembly in assemblies:
                if parent.kit_serialnumber == assembly.kit_serialnumber:
                    messages.success(request, 'An assembly with this serial number already exist')
                    return render(request, 'inventory/assembly/kit_clone.html', context)
            parent.save()
            piece_instance = [kit.piece_kit_1, kit.piece_kit_2, kit.piece_kit_3, kit.piece_kit_4, kit.piece_kit_5,
                              kit.piece_kit_6, kit.piece_kit_7, kit.piece_kit_8, kit.piece_kit_9, kit.piece_kit_10,
                              kit.piece_kit_11, kit.piece_kit_12, kit.piece_kit_13, kit.piece_kit_14, kit.piece_kit_15]
            for item in piece_instance:
                if item is not None:
                    for instance in instances:
                        if instance == item:
                            instance.update_comment = kit.update_comment
                            instance.first_location = kit.first_location
                            instance.second_location = kit.second_location
                            instance.third_location = kit.third_location
                            instance.fourth_location = kit.fourth_location
                            instance.fifth_location = kit.fifth_location
                            instance.sixth_location = kit.sixth_location
                            instance.seventh_location = kit.seventh_location
                            instance.eighth_location = kit.eighth_location
                            instance.status = kit.kit_status
                            instance.save()
            return redirect(kit.get_absolute_url())
    else:
        form = KitForm(instance=kit)
    context = {
        'kit': kit,
        'form': form,
    }
    return render(request, 'inventory/assembly/kit_clone.html', context)


# Display Kit List
class KitList(ListView):
    """
    List of Kits
    """
    model = Kit
    paginate_by = 10
    template_name = 'inventory/assembly/kit_list.html'  # Template location

    def get_context_data(self, **kwargs):
        """
        Returns context data for displaying the list of objects.
        :rtype: list
        """
        # Call the base implementation first to get the context
        context = super(KitList, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['kit'] = Kit.objects.all().order_by('-id')
        return context


# Display a specific Kit
def show_kit(request, primary_key):
    """
    Function to display Kit detail and the PieceInstances it contains
    :rtype: Kit, PieceInstance
    """
    kit = Kit.objects.get(pk=primary_key)
    piece_instance = [kit.piece_kit_1, kit.piece_kit_2, kit.piece_kit_3, kit.piece_kit_4, kit.piece_kit_5,
                    kit.piece_kit_6, kit.piece_kit_7, kit.piece_kit_8, kit.piece_kit_9, kit.piece_kit_10,
                    kit.piece_kit_11, kit.piece_kit_12, kit.piece_kit_13, kit.piece_kit_14, kit.piece_kit_15]
    context = {'kit': kit, 'piece_instance': piece_instance}
    return render(request, 'inventory/assembly/kit_detail.html', context)


# Movement Management Section

def movement_exchange(request):
    """
    Function to display MovementForm
    :rtype: MovementForm
    """
    form = MovementForm(request.POST or None)
    # items = PieceInstance.objects.all().order_by('serial_number')
    context = {
        'form': form,
        # 'items': items,
    }
    if form.is_valid():
        obj = form.save(commit=False)
        # Store old location and status
        obj.old_first_location = obj.item_2.first_location
        obj.old_second_location = obj.item_2.second_location
        obj.old_third_location = obj.item_2.third_location
        obj.old_fourth_location = obj.item_2.fourth_location
        obj.old_fifth_location = obj.item_2.fifth_location
        obj.old_sixth_location = obj.item_2.sixth_location
        obj.old_seventh_location = obj.item_2.seventh_location
        obj.old_eighth_location = obj.item_2.eighth_location
        obj.old_status = obj.item_2.status
        # Update location of the item being replaced with the item it replaces
        # Check if replaced object is in Assembly
        try:
            kit = Kit.objects.get(
                Q(piece_kit_1=obj.item_1) | Q(piece_kit_2=obj.item_1) | Q(piece_kit_3=obj.item_1) | Q(
                    piece_kit_4=obj.item_1)
                | Q(piece_kit_5=obj.item_1) | Q(piece_kit_6=obj.item_1) | Q(piece_kit_7=obj.item_1) | Q(
                    piece_kit_8=obj.item_1)
                | Q(piece_kit_9=obj.item_1) | Q(piece_kit_10=obj.item_1) | Q(piece_kit_11=obj.item_1) | Q(
                    piece_kit_12=obj.item_1)
                | Q(piece_kit_13=obj.item_1) | Q(piece_kit_14=obj.item_1) | Q(piece_kit_15=obj.item_1))
        except:
            kit = None

        if kit:
            if kit.piece_kit_1 == obj.item_1:
                kit.piece_kit_1 = obj.item_2
            elif kit.piece_kit_2 == obj.item_1:
                kit.piece_kit_2 = obj.item_2
            elif kit.piece_kit_3 == obj.item_1:
                kit.piece_kit_3 = obj.item_2
            elif kit.piece_kit_4 == obj.item_1:
                kit.piece_kit_4 = obj.item_2
            elif kit.piece_kit_5 == obj.item_1:
                kit.piece_kit_5 = obj.item_2
            elif kit.piece_kit_6 == obj.item_1:
                kit.piece_kit_6 = obj.item_2
            elif kit.piece_kit_7 == obj.item_1:
                kit.piece_kit_7 = obj.item_2
            elif kit.piece_kit_8 == obj.item_1:
                kit.piece_kit_8 = obj.item_2
            elif kit.piece_kit_9 == obj.item_1:
                kit.piece_kit_9 = obj.item_2
            elif kit.piece_kit_10 == obj.item_1:
                kit.piece_kit_10 = obj.item_2
            elif kit.piece_kit_11 == obj.item_1:
                kit.piece_kit_11 = obj.item_2
            elif kit.piece_kit_12 == obj.item_1:
                kit.piece_kit_12 = obj.item_2
            elif kit.piece_kit_13 == obj.item_1:
                kit.piece_kit_13 = obj.item_2
            elif kit.piece_kit_14 == obj.item_1:
                kit.piece_kit_14 = obj.item_2
            elif kit.piece_kit_15 == obj.item_1:
                kit.piece_kit_15 = obj.item_2
            kit.save()

        obj.item_2.first_location = obj.item_1.first_location
        obj.item_2.second_location = obj.item_1.second_location
        obj.item_2.third_location = obj.item_1.third_location
        obj.item_2.fourth_location = obj.item_1.fourth_location
        obj.item_2.fifth_location = obj.item_1.fifth_location
        obj.item_2.sixth_location = obj.item_1.sixth_location
        obj.item_2.seventh_location = obj.item_1.seventh_location
        obj.item_2.eighth_location = obj.item_1.eighth_location
        # Update status of the item being replaced with the item it replaces
        obj.item_2.status = obj.item_1.status
        # Put object being replaced in waiting zone
        obj.item_1.first_location = First_location.objects.get(name='Waiting')
        obj.item_1.second_location = None
        obj.item_1.third_location = None
        obj.item_1.fourth_location = None
        obj.item_1.fifth_location = None
        obj.item_1.sixth_location = None
        obj.item_1.seventh_location = None
        obj.item_1.eighth_location = None
        # Update status of the object being replaced
        obj.item_1.status = 'Waiting'
        # Both objects update comments take the comment of the movement
        obj.item_1.update_comment = obj.update_comment_item1
        obj.item_2.update_comment = obj.update_comment_item2
        obj.item_1.date_update = datetime.date.today()
        obj.item_2.date_update = datetime.date.today()
        # Save the objects
        obj.item_1.save()
        obj.item_2.save()
        # Save the movement
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, 'inventory/movement/movement_choice.html', context)


def movement_detail(request, primary_key):
    """
    Function to display Movement detail
    :rtype: MovementExchange
    """
    movement = MovementExchange.objects.get(pk=primary_key)
    context = {'movement': movement}
    return render(request, 'inventory/movement/movement_detail.html', context)


def movement_list(request):
    """
    Returns the list of MovementExchanges
    :rtype: list
    """
    movements = MovementExchange.objects.order_by('date_created')
    context = {'movements': movements}
    return render(request, 'inventory/movement/movement_list.html', context)


def movement_revert(request, movement_id):
    """
    Function to revert a MovementExchange
    :rtype: MovementExchange
    """
    movement = MovementExchange.objects.get(id=movement_id)
    # We check if the replaced item was in an assembly
    # Check if replaced object is in Assembly
    try:
        kit = Kit.objects.get(
            Q(piece_kit_1=movement.item_2) | Q(piece_kit_2=movement.item_2) | Q(piece_kit_3=movement.item_2) | Q(
                piece_kit_4=movement.item_2)
            | Q(piece_kit_5=movement.item_2) | Q(piece_kit_6=movement.item_2) | Q(piece_kit_7=movement.item_2) | Q(
                piece_kit_8=movement.item_2)
            | Q(piece_kit_9=movement.item_2) | Q(piece_kit_10=movement.item_2) | Q(piece_kit_11=movement.item_2) | Q(
                piece_kit_12=movement.item_2)
            | Q(piece_kit_13=movement.item_2) | Q(piece_kit_14=movement.item_2) | Q(piece_kit_15=movement.item_2))
    except:
        kit = None

    if kit:
        if kit.piece_kit_1 == movement.item_2:
            kit.piece_kit_1 = movement.item_1
        elif kit.piece_kit_2 == movement.item_2:
            kit.piece_kit_2 = movement.item_1
        elif kit.piece_kit_3 == movement.item_2:
            kit.piece_kit_3 = movement.item_1
        elif kit.piece_kit_4 == movement.item_2:
            kit.piece_kit_4 = movement.item_1
        elif kit.piece_kit_5 == movement.item_2:
            kit.piece_kit_5 = movement.item_1
        elif kit.piece_kit_6 == movement.item_2:
            kit.piece_kit_6 = movement.item_1
        elif kit.piece_kit_7 == movement.item_2:
            kit.piece_kit_7 = movement.item_1
        elif kit.piece_kit_8 == movement.item_2:
            kit.piece_kit_8 = movement.item_1
        elif kit.piece_kit_9 == movement.item_2:
            kit.piece_kit_9 = movement.item_1
        elif kit.piece_kit_10 == movement.item_2:
            kit.piece_kit_10 = movement.item_1
        elif kit.piece_kit_11 == movement.item_2:
            kit.piece_kit_11 = movement.item_1
        elif kit.piece_kit_12 == movement.item_2:
            kit.piece_kit_12 = movement.item_1
        elif kit.piece_kit_13 == movement.item_2:
            kit.piece_kit_13 = movement.item_1
        elif kit.piece_kit_14 == movement.item_2:
            kit.piece_kit_14 = movement.item_1
        elif kit.piece_kit_15 == movement.item_2:
            kit.piece_kit_15 = movement.item_1
        kit.save()

    movement.item_1.first_location = movement.item_2.first_location
    movement.item_1.second_location = movement.item_2.second_location
    movement.item_1.third_location = movement.item_2.third_location
    movement.item_1.fourth_location = movement.item_2.fourth_location
    movement.item_1.fifth_location = movement.item_2.fifth_location
    movement.item_1.sixth_location = movement.item_2.sixth_location
    movement.item_1.seventh_location = movement.item_2.seventh_location
    movement.item_1.eighth_location = movement.item_2.eighth_location
    movement.item_1.status = movement.item_2.status
    movement.item_1.date_update = datetime.date.today()
    movement.item_1.save()
    movement.item_2.first_location = movement.old_first_location
    movement.item_2.second_location = movement.old_second_location
    movement.item_2.third_location = movement.old_third_location
    movement.item_2.fourth_location = movement.old_fourth_location
    movement.item_2.fifth_location = movement.old_fifth_location
    movement.item_2.sixth_location = movement.old_sixth_location
    movement.item_2.seventh_location = movement.old_seventh_location
    movement.item_2.eighth_location = movement.old_eighth_location
    movement.item_2.status = movement.old_status
    movement.item_2.date_update = datetime.date.today()
    movement.item_2.save()
    movement.revert_button = False
    movement.save()

    context = {'movement': movement}
    return render(request, 'inventory/movement/movement_detail.html', context)


# Equivalence Management
def create_equivalence(request):
    """
    Function to display EquivalenceForm
    :rtype: EquivalenceForm
    """
    forms = EquivalenceForm()
    if request.method == 'POST':
        forms = EquivalenceForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('equivalence-list')
    context = {
        'form': forms
    }
    return render(request, 'inventory/equivalence/create_equivalence.html', context)


# Display a list of all the Pieces in the inventory
class EquivalenceListView(ListView):
    """
    List of Equivalences
    """
    model = Equivalence
    paginate_by = 10
    template_name = 'inventory/equivalence/equivalence_list.html'  # Template location

    def get_context_data(self, **kwargs):
        """
        Returns context data for displaying the list of objects.
        :rtype: list
        """
        # Call the base implementation first to get the context
        context = super(EquivalenceListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['equivalence'] = Equivalence.objects.all().order_by('-id')
        return context


def equivalence_detail(request, primary_key):
    """
    Function to display Equivalence detail and the Pieces it is about
    :rtype: Equivalence, Piece
    """
    equivalence = Equivalence.objects.get(pk=primary_key)
    pieces = [equivalence.pieceeq_1, equivalence.pieceeq_2, equivalence.pieceeq_3, equivalence.pieceeq_4,
              equivalence.pieceeq_5, equivalence.pieceeq_6, equivalence.pieceeq_7, equivalence.pieceeq_8,
              equivalence.pieceeq_9, equivalence.pieceeq_10, equivalence.pieceeq_11, equivalence.pieceeq_12,
              equivalence.pieceeq_13, equivalence.pieceeq_14, equivalence.pieceeq_15]
    context = {'equivalence': equivalence, 'pieces': pieces}
    return render(request, 'inventory/equivalence/equivalence_detail.html', context)


# Update an instance
def update_equivalence(request, equivalence_id):
    """
    Function to update Equivalence
    :rtype: MovementForm, MovementExchange
    """
    equivalence = Equivalence.objects.get(pk=equivalence_id)
    if request.method == "POST":
        form = EquivalenceForm(request.POST, instance=equivalence)
        if form.is_valid():
            form.save()
            return redirect(equivalence.get_absolute_url())
    else:
        form = EquivalenceForm(instance=equivalence)
    context = {'equivalence': equivalence, 'form': form}
    return render(request, 'inventory/equivalence/equivalence_update.html', context)


# Display history of specific Consumable
def show_consumable_history(request, primary_key):
    """
    Function to display Consumable full history
    :rtype: list, Consumable
    """
    consumable = Consumable.objects.get(pk=primary_key)
    history = consumable.history.all()
    context = {'history': history, 'consumable': consumable}
    return render(request, 'inventory/consumable/consumable_history.html', context)


# Display history of a specific Piece
def show_piece_history(request, primary_key):
    """
    Function to display Piece full history
    :rtype: list, Piece
    """
    piece = Piece.objects.get(pk=primary_key)
    history = piece.history.all()
    context = {'history': history, 'piece': piece}
    return render(request, 'inventory/piece/piece_history.html', context)


# Display history of a specific Instance
def show_instance_history(request, primary_key):
    """
    Function to display PieceInstance full history
    :rtype: list, PieceInstance
    """
    piece_instance = PieceInstance.objects.get(pk=primary_key)
    history = piece_instance.history.all()
    context = {'history': history, 'piece_instance': piece_instance}
    return render(request, 'inventory/instances/instance_history.html', context)


# Display history of a specific Assembly
def show_assembly_history(request, primary_key):
    """
    Function to display Assembly full history
    :rtype: list, Assembly
    """
    assembly = Kit.objects.get(pk=primary_key)
    history = assembly.history.all()
    context = {'history': history, 'assembly': assembly}
    return render(request, 'inventory/assembly/assembly_history.html', context)


