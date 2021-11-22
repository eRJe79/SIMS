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
def load_item_1(request):
    piece_id = request.GET.get('piece')
    myitems = PieceInstance.objects.filter(piece_id=piece_id).order_by('serial_number')
    # We don't want items that are in stock
    items = []
    for item in myitems:
        if item.status != 'In Stock':
            items.append(item)
    return render(request, 'hr/item_dropdown_list_options.html', {'items': items})


def load_item_2(request):
    piece_id = request.GET.get('piece')
    myitems = PieceInstance.objects.filter(piece_id=piece_id).order_by('serial_number')
    items = myitems.filter(Q(status='In Stock') | Q(status = 'On Test'))
    return render(request, 'hr/item_dropdown_list_options.html', {'items': items})


def load_piece_kit(request):
    piece_id = request.GET.get('piece')
    items = PieceInstance.objects.filter(piece_id=piece_id).order_by('serial_number')
    return render(request, 'hr/item_dropdown_list_options.html', {'items': items})


# Location dependencies management
def load_second_location(request):
    first_loc_id = request.GET.get('previous_loc')
    second_loc = Second_location.objects.filter(previous_loc_id=first_loc_id).order_by('name')
    return render(request, 'hr/second_loc_dropdown_list_options.html', {'second_loc': second_loc})


def load_third_location(request):
    second_loc_id = request.GET.get('previous_loc')
    third_loc = Third_location.objects.filter(previous_loc_id=second_loc_id).order_by('name')
    return render(request, 'hr/third_loc_dropdown_list_options.html', {'third_loc': third_loc})


def load_fourth_location(request):
    third_loc_id = request.GET.get('previous_loc')
    fourth_loc = Fourth_location.objects.filter(previous_loc_id=third_loc_id).order_by('name')
    return render(request, 'hr/fourth_loc_dropdown_list_options.html', {'fourth_loc': fourth_loc})


def load_fifth_location(request):
    fourth_loc_id = request.GET.get('previous_loc')
    fifth_loc = Fifth_location.objects.filter(previous_loc_id=fourth_loc_id).order_by('name')
    return render(request, 'hr/fifth_loc_dropdown_list_options.html', {'fifth_loc': fifth_loc})


def load_sixth_location(request):
    fifth_loc_id = request.GET.get('previous_loc')
    sixth_loc = Sixth_location.objects.filter(previous_loc_id=fifth_loc_id).order_by('name')
    return render(request, 'hr/sixth_loc_dropdown_list_options.html', {'sixth_loc': sixth_loc})


def load_seventh_location(request):
    sixth_loc_id = request.GET.get('previous_loc')
    seventh_loc = Seventh_location.objects.filter(previous_loc_id=sixth_loc_id).order_by('name')
    return render(request, 'hr/seventh_loc_dropdown_list_options.html', {'seventh_loc': seventh_loc})


def load_eighth_location(request):
    seventh_loc_id = request.GET.get('previous_loc')
    eighth_loc = Eighth_location.objects.filter(previous_loc_id=seventh_loc_id).order_by('name')
    return render(request, 'hr/eighth_loc_dropdown_list_options.html', {'eighth_loc': eighth_loc})


# Export database to csv
# Generate CSV File Instance List
def database_csv(request):
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
def shipped_received_csv(request):
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


def reparation_record_csv(request):
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
                # We check that the hitory is between the start and end date
                for h in myhistory:
                    if start_date <= h.history_date.date() <= end_date:
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


def movement_record_csv(request):
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
                        'Replacing Piece', 'PE CAE Part Number', 'RP CAE Serial Number', 'RP Comment',
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
def low_stock_record_csv(request):
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
    template_name = 'inventory/consumable/create_consumable.html'
    model = Consumable
    form_class = ConsumableForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = ConsumableForm()
        context = {
            'form': form,
        }
        return render(request, 'inventory/consumable/create_consumable.html', context)

    def post(self, request, *args, **kwargs):
        # # if our ajax is calling so we have to take action
        # # because this is not the form submission
        # if request.is_ajax():
        #     cp = request.POST.copy()  # because we couldn't change fields values directly in request.POST
        #     value = int(cp['wtd'])  # figure out if the process is addition or deletion
        #     prefix = "instance_reverse"
        #     cp[f'{prefix}-TOTAL_FORMS'] = int(
        #         cp[f'{prefix}-TOTAL_FORMS']) + value
        #     formset = PieceInstancePieceFormSet(cp)  # catch any data which were in the previous formsets and deliver to-
        #     # the new formsets again -> if the process is addition!
        #     return render(request, 'inventory/formset.html', {'formset': formset})

        self.object = None
        form_class = self.get_form_class()
        form = ConsumableForm(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        # instance_form.instance = self.object
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


# Display specific consumable
def show_consumable(request, primary_key):
    consumable = Consumable.objects.get(pk=primary_key)
    context = {'consumable': consumable}
    return render(request, 'inventory/consumable/consumable_detail.html', context)


def consumable_list(request):
    consumable_list = Consumable.objects.all().order_by('name')
    return render(request, 'inventory/consumable/consumable_list.html', {'consumable_list': consumable_list})


# Update a consumable
def update_consumable(request, consumable_id):
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
    template_name = 'inventory/piece/create_piece.html'
    model = Piece
    form_class = PieceForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = PieceForm()
        context = {
            'form': form,
        }
        return render(request, 'inventory/piece/create_piece.html', context)

    def post(self, request, *args, **kwargs):
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
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        # instance_form.instance = self.object
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


# Display a list of all the Pieces in the inventory
class PieceListView(ListView):
    model = Piece
    paginate_by = 10
    template_name = 'inventory/piece/piece_list.html'  # Template location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PieceListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['piece'] = Piece.objects.all().order_by('-id')
        return context


# Display a specific Piece
def show_piece(request, primary_key):
    piece = Piece.objects.get(pk=primary_key)
    piece_instance = PieceInstance.objects.all().order_by('status')
    # Instance management
    instance_installed = PieceInstance.objects.filter(status='Installed', piece=piece).count()
    instance_in_stock = PieceInstance.objects.filter(status='In Stock', piece=piece).count()
    instance_discarded = PieceInstance.objects.filter(status='Discarded', piece=piece).count()
    instance_in_reparation = PieceInstance.objects.filter(status='In Repair', piece=piece).count()
    # Equivalence management
    try:
        equivalences = Equivalence.objects.get(Q(pieceeq_1=piece) | Q(pieceeq_2=piece) | Q(pieceeq_3=piece)| Q(pieceeq_4=piece)
                                       | Q(pieceeq_5=piece) | Q(pieceeq_6=piece) | Q(pieceeq_7=piece)| Q(pieceeq_8=piece)
                                       | Q(pieceeq_9=piece) | Q(pieceeq_10=piece) | Q(pieceeq_11=piece)| Q(pieceeq_12=piece)
                                       | Q(pieceeq_13=piece) | Q(pieceeq_14=piece) | Q(pieceeq_15=piece))
    except:
        equivalences = None
    piece_eq_list = equivalences
    context = {'piece': piece, 'piece_instance': piece_instance, 'instance_installed': instance_installed,
               'instance_in_stock': instance_in_stock, 'instance_discarded': instance_discarded,
               'instance_in_reparation': instance_in_reparation, 'piece_eq_list': piece_eq_list}
    return render(request, 'inventory/piece/piece_detail.html', context)


# Update a piece
def update_piece(request, piece_id):
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
    piece = Piece.objects.get(pk=piece_id)
    piece.pk=None
    piece.update_comment = ''
    if request.method == "POST":
        form = PieceForm(request.POST, request.FILES, instance=piece)
        if form.is_valid():
            form.save()
            return redirect(piece.get_absolute_url())
    else:
        form = PieceForm(instance=piece)
    context = {'piece': piece, 'form': form}
    return render(request, 'inventory/piece/clone_piece.html', context)


# Instance creation
class PieceInstanceCreate(CreateView):
    template_name = 'inventory/instance/create_instance_piece.html'
    model = PieceInstance
    form_class = PieceInstanceForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = PieceInstanceForm()
        context = {
            'form': form,
        }
        return render(request, 'inventory/instance/create_instance_piece.html', context)

    def post(self, request, *args, **kwargs):
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
        files = request.FILES.getlist('update_document')
        if form.is_valid():
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def form_valid(self, request, form):
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
        return self.render_to_response(
            self.get_context_data(form=form))


def all_piece_instance(request):
    piece_instance_list = PieceInstance.objects.all().order_by('piece')
    return render(request, 'inventory/instance/piece_instance_list.html', {'piece_instance_list': piece_instance_list})


# Display specific instance information
def show_instance_form(request, primary_key):
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
    return render(request, 'inventory/instance/piece_instance_detail.html', context)


# Display instances and assembly as list
def show_instance_assembly_list(request):
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
    return render(request, 'inventory/instance/update_piece_instance.html', context)


# clone an instance
def clone_instance(request, instance_id):
    piece_instance = PieceInstance.objects.get(pk=instance_id)
    piece_instance.update_comment = ''
    if request.method == "POST":
        form = PieceInstanceForm(request.POST, request.FILES, instance=piece_instance)
        piece_instance.pk=None
        if form.is_valid():
            form.save()
            return redirect(piece_instance.get_absolute_url())
    else:
        form = PieceInstanceForm(instance=piece_instance)
    context = {'piece_instance': piece_instance, 'form': form}
    return render(request, 'inventory/instance/clone_existing_piece.html', context)


# Delete an instance
def delete_instance(request, instance_id):
    piece_instance = PieceInstance.objects.get(pk=instance_id)
    piece_instance.delete()
    return redirect('piece-detail')


# Search feature
# Specific to Consumable
def search_consumable_database(request):
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
    if request.method == "POST":
        searched = request.POST['searched']
        results_instance = []
        results_assemblies = []
        if searched == 'RSPL' or searched == 'rspl':
            for i in PieceInstance.objects.filter(is_rspl=True):
                results_instance.append(i)
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
            results = (results_assemblies + results_instance)
        context = {'searched': searched, 'results': results}
        return render(request, 'inventory/search/search_general.html', context)
    else:
        return render(request, 'inventory/search/search_general.html', {})


# Assembly Management Section
# Create Group Assembly
class GroupAssemblyCreate(CreateView):
    template_name = 'inventory/group_assembly/create_groupassembly.html'
    model = GroupAssembly
    form_class = GroupAssemblyForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = GroupAssemblyForm()
        context = {
            'form': form,
        }
        return render(request, 'inventory/group_assembly/create_groupassembly.html', context)

    def post(self, request, *args, **kwargs):
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
        form = GroupAssemblyForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        # instance_form.instance = self.object
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


# Display a list of all the Pieces in the inventory
class GroupAssemblyListView(ListView):
    model = GroupAssembly
    paginate_by = 10
    template_name = 'inventory/group_assembly/groupassembly_list.html'  # Template location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(GroupAssemblyListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['groupassembly'] = GroupAssembly.objects.all().order_by('-id')
        return context


# Display a specific Group Assembly
def show_groupassembly(request, primary_key):
    groupassembly = GroupAssembly.objects.get(pk=primary_key)
    kit = Kit.objects.all().order_by('name')
    context = {'groupassembly': groupassembly, 'kit': kit}
    return render(request, 'inventory/group_assembly/groupassembly_detail.html', context)


# Create new assembly
class KitCreate(CreateView):
    template_name = 'inventory/assembly/kit_form.html'
    model = Kit
    form_class = KitForm

    def form_valid(self, form):
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


# Display Kit List
class KitList(ListView):
    model = Kit
    paginate_by = 10
    template_name = 'inventory/assembly/kit_list.html'  # Template location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(KitList, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['kit'] = Kit.objects.all().order_by('-id')
        return context


# Display a specific Kit
def show_kit(request, primary_key):
    kit = Kit.objects.get(pk=primary_key)
    piece_instance = [kit.piece_kit_1, kit.piece_kit_2, kit.piece_kit_3, kit.piece_kit_4, kit.piece_kit_5,
                    kit.piece_kit_6, kit.piece_kit_7, kit.piece_kit_8, kit.piece_kit_9, kit.piece_kit_10,
                    kit.piece_kit_11, kit.piece_kit_12, kit.piece_kit_13, kit.piece_kit_14, kit.piece_kit_15]
    context = {'kit': kit, 'piece_instance': piece_instance}
    return render(request, 'inventory/assembly/kit_detail.html', context)


# Movement Management Section

def movement_exchange(request):
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
        kit.save()
        return redirect(obj.get_absolute_url())
    return render(request, 'inventory/movement/movement_choice.html', context)


def movement_detail(request, primary_key):
    movement = MovementExchange.objects.get(pk=primary_key)
    context = {'movement': movement}
    return render(request, 'inventory/movement/movement_detail.html', context)


def movement_list(request):
    movements = MovementExchange.objects.order_by('date_created')
    context = {'movements': movements}
    return render(request, 'inventory/movement/movement_list.html', context)


def movement_revert(request, movement_id):
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
    kit.save()

    context = {'movement': movement}
    return render(request, 'inventory/movement/movement_detail.html', context)


# Equivalence Management
def create_equivalence(request):
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
    model = Equivalence
    paginate_by = 10
    template_name = 'inventory/equivalence/equivalence_list.html'  # Template location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(EquivalenceListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['equivalence'] = Equivalence.objects.all().order_by('-id')
        return context


def equivalence_detail(request, primary_key):
    equivalence = Equivalence.objects.get(pk=primary_key)
    context = {'equivalence': equivalence}
    return render(request, 'inventory/equivalence/equivalence_detail.html', context)


# Update an instance
def update_equivalence(request, equivalence_id):
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
    consumable = Consumable.objects.get(pk=primary_key)
    history = consumable.history.all()
    context = {'history': history, 'consumable': consumable}
    return render(request, 'inventory/consumable/consumable_history.html', context)


# Display history of a specific Piece
def show_piece_history(request, primary_key):
    piece = Piece.objects.get(pk=primary_key)
    history = piece.history.all()
    context = {'history': history, 'piece': piece}
    return render(request, 'inventory/piece/piece_history.html', context)


# Display history of a specific Instance
def show_instance_history(request, primary_key):
    piece_instance = PieceInstance.objects.get(pk=primary_key)
    history = piece_instance.history.all()
    context = {'history': history, 'piece_instance': piece_instance}
    return render(request, 'inventory/instance/instance_history.html', context)


# Display history of a specific Assembly
def show_assembly_history(request, primary_key):
    assembly = Kit.objects.get(pk=primary_key)
    history = assembly.history.all()
    context = {'history': history, 'assembly': assembly}
    return render(request, 'inventory/assembly/assembly_history.html', context)


