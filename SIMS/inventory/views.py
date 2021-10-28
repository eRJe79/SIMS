import csv

from django.db import transaction
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from simple_history.utils import update_change_reason
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.utils.translation import ugettext as _
from django.db.models import Q


from .models import (
    Equivalence,
    Piece,
    PieceInstance,
    GroupAssembly,
    Kit,
    First_location,
    Second_location,
    Third_location,
    Fourth_location,
    Fifth_location,
    Sixth_location,
    Seventh_location,
    Eighth_location,
    Mptt,
    MovementExchange,
)

from .forms import (
    PieceForm,
    PieceInstanceForm,
    PieceInstancePieceFormSet,
    KitGroupAssemblyFormSet,
    GroupAssemblyForm,
    KitForm,
    MovementForm,
    EquivalenceForm,
)

# Movement dependencies management
def load_item_1(request):
    print("item 1")
    piece_id = request.GET.get('piece')
    print(piece_id)
    items = PieceInstance.objects.filter(piece_id=piece_id).order_by('serial_number')
    print(items)
    return render(request, 'hr/item_dropdown_list_options.html', {'items': items})

def load_item_2(request):
    piece_id = request.GET.get('piece')
    myitems = PieceInstance.objects.filter(piece_id=piece_id).order_by('serial_number')
    items_instock = myitems.filter(status='In Stock')
    items_ontest = myitems.filter(status='On Test')
    items = myitems.filter(Q(status='In Stock') | Q(status = 'On Test'))
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

    # Designate The Model
    instances = PieceInstance.objects.all().order_by('piece')

    # Add column headings to the csv file
    writer.writerow(['Piece model', 'Manufacturer', 'Manufacturer Part Number', 'Manufacturer Serial Number',
                       'Website',
                     'Description', 'Documentation', 'Calibration Recurrence', 'Type', 'Characteristic', 'Owner',
                     'Restriction', 'RSPL', 'Assembly Name', 'CAE Part Number', 'CAE Serial Number', 'OEM',
                     'OEM Part Number', 'Provider Serial Number',
                     'First Location', 'Second Location', 'Third Location', 'Fourth Location', 'Fifth Location',
                     'Sixth Location', 'Seventh Location', 'Eighth Location',
                     'Status', 'Date created', 'Last Update',
                     'Next calibration date', 'End of life', 'End of guarantee'])

    # Loop Through instance and output
    for instance in instances:
        if instance.is_rspl:
            rspl = 'RSPL'
        elif not instance.is_rspl:
            rspl = 'Not RSPL'

        writer.writerow([instance.piece.piece_model, instance.piece.manufacturer, instance.piece.manufacturer_part_number,
                         instance.manufacturer_serialnumber, instance.piece.website, instance.piece.description,
                         instance.piece.documentation, instance.piece.calibration_recurrence,
                         instance.piece.item_type, instance.piece.item_characteristic, instance.owner,
                         instance.restriction, rspl, instance.kit, instance.piece.cae_part_number, instance.serial_number,
                         instance.piece.provider, instance.piece.provider_part_number,  instance.provider_serialnumber,
                         instance.first_location, instance.second_location, instance.third_location, instance.fourth_location,
                         instance.fifth_location, instance.sixth_location, instance.seventh_location, instance.eighth_location,
                         instance.status, instance.date_created, instance.date_update,
                         instance.date_calibration, instance.date_end_of_life, instance.date_guarantee])
    return response

def tree(request):
    tree_level = Mptt.objects.all()
    context = {'tree_level': tree_level}
    return render(request, 'inventory/tree.html', context)


class PieceCreate(CreateView):
    template_name = 'inventory/create_piece.html'
    model = Piece
    form_class = PieceForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = PieceForm()
        context = {
            'form': form,
        }
        return render(request, 'inventory/create_piece.html', context)

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
    template_name = 'inventory/piece_list.html'  # Template location

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
    print(equivalences)
    piece_eq_list = equivalences
    context = {'piece': piece, 'piece_instance': piece_instance, 'instance_installed': instance_installed,
               'instance_in_stock': instance_in_stock, 'instance_discarded': instance_discarded,
               'instance_in_reparation': instance_in_reparation, 'piece_eq_list': piece_eq_list}
    return render(request, 'inventory/piece_detail.html', context)

class PieceInstanceCreate(CreateView):
    template_name = 'inventory/create_instance_piece.html'
    model = PieceInstance
    form_class = PieceInstanceForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = PieceInstanceForm()
        context = {
            'form': form,
        }
        return render(request, 'inventory/create_instance_piece.html', context)

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
        print(piece_instance)
        self.object = form.save(commit=False)
        print(piece_instance)
        for instance in piece_instance:
            if self.object.piece == instance.piece:
                print(instance.serial_number)
                print(self.object.serial_number)
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
    return render(request, 'inventory/piece_instance_list.html', {'piece_instance_list': piece_instance_list})

# Display specific instance information
def show_instance_form(request, primary_key):
    piece_instance = PieceInstance.objects.get(pk=primary_key)
    context = {'piece_instance': piece_instance}
    return render(request, 'inventory/piece_instance_detail.html', context)

# Display instances and assembly as list
def show_instance_assembly_list(request):
    # We create 2 lists to regroup objects from pieceInstance and Kit
    myinstancelist=[]
    myassemblylist=[]
    for i in PieceInstance.objects.all():
        myinstancelist.append(i)
    for i in Kit.objects.all():
        myassemblylist.append(i)
    print(myinstancelist, myassemblylist)
    # We assemble one list under one for display purpose
    mylist = (myinstancelist + myassemblylist)
    print(mylist)
    context = {'mylist': mylist}
    return render(request, 'inventory/general_list.html', context)

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
    return render(request, 'inventory/update_piece.html', context)

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
    return render(request, 'inventory/clone_piece.html', context)

# Update an instance
def update_instance(request, instance_id):
    piece_instance = PieceInstance.objects.get(pk=instance_id)
    piece_instance.date_update = timezone.now()
    piece_instance.update_comment = ''
    if request.method == "POST":
        form = PieceInstanceForm(request.POST, request.FILES, instance=piece_instance)
        if form.is_valid():
            form.save()
            return redirect(piece_instance.get_absolute_url())
    else:
        form = PieceInstanceForm(instance=piece_instance)
    context = {'piece_instance': piece_instance, 'form': form}
    return render(request, 'inventory/update_piece_instance.html', context)

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
    return render(request, 'inventory/clone_existing_piece.html', context)

# Delete an instance
def delete_instance(request, instance_id):
    piece_instance = PieceInstance.objects.get(pk=instance_id)
    piece_instance.delete()
    return redirect('piece-detail')


# Search feature
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
                                       | Q(item_characteristic__contains=searched)
                                       )
        context = {'searched': searched, 'results': results}
        return render(request, 'inventory/search.html', context)
    else:
        return render(request, 'inventory/search.html', {})

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
        return render(request, 'inventory/search_instance.html', context)
    else:
        return render(request, 'inventory/search_instance.html', {})

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
        return render(request, 'inventory/search_groupassembly.html', context)
    else:
        return render(request, 'inventory/search_groupassembly.html', {})

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
        return render(request, 'inventory/search_assembly.html', context)
    else:
        return render(request, 'inventory/search_assembly.html', {})

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
        return render(request, 'inventory/search_general.html', context)
    else:
        return render(request, 'inventory/search_general.html', {})

# Assembly Management Section
# Create Group Assembly
class GroupAssemblyCreate(CreateView):
    template_name = 'inventory/create_groupassembly.html'
    model = GroupAssembly
    form_class = GroupAssemblyForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = GroupAssemblyForm()
        context = {
            'form': form,
        }
        return render(request, 'inventory/create_groupassembly.html', context)

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
    template_name = 'inventory/groupassembly_list.html'  # Template location

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
    return render(request, 'inventory/groupassembly_detail.html', context)

#Create new assembly
class KitCreate(CreateView):
    template_name = 'inventory/kit_form.html'
    model = Kit

    def get(self, request, *args, **kwargs):
        self.object = None
        form = KitForm(request.POST)
        context = {
            'form': KitForm(),
        }
        return render(request, 'inventory/kit_form.html', context)

    def post(self, request, *args, **kwargs):
        # if our ajax is calling so we have to take action
        # because this is not the form submission
        self.object = None
        form = KitForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))

# Update an assembly
def update_kit(request, kit_id):
    kit = Kit.objects.get(pk=kit_id)
    kit.date_update = timezone.now()
    kit.update_comment = ''
    piece_instance = [kit.piece_kit_1, kit.piece_kit_2, kit.piece_kit_3, kit.piece_kit_4, kit.piece_kit_5,
                      kit.piece_kit_6, kit.piece_kit_7, kit.piece_kit_8, kit.piece_kit_9, kit.piece_kit_10,
                      kit.piece_kit_11, kit.piece_kit_12, kit.piece_kit_13, kit.piece_kit_14, kit.piece_kit_15]
    form = KitForm(request.POST or None, instance=kit)
    context = {
        'kit': kit,
        'form': form,
    }
    if form.is_valid():
        parent = form.save(commit=False)
        for item in piece_instance:
            if item is not None:
                item.update_comment = kit.update_comment
                item.first_location = kit.first_location
                item.second_location = kit.second_location
                item.third_location = kit.third_location
                item.fourth_location = kit.fourth_location
                item.fifth_location = kit.fifth_location
                item.sixth_location = kit.sixth_location
                item.seventh_location = kit.seventh_location
                item.eighth_location = kit.eighth_location
                item.status = kit.kit_status
                item.save()
        parent.save()
        return redirect(kit.get_absolute_url())
    return render(request, 'inventory/kit_update.html', context)


# Display Kit List
class KitList(ListView):
    model = Kit
    paginate_by = 10
    template_name = 'inventory/kit_list.html'  # Template location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(KitList, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['kit'] = Kit.objects.all().order_by('-id')
        return context

# Display a specific Kit
def show_kit(request, primary_key):
    kit = Kit.objects.get(pk=primary_key)
    piece_instance=[kit.piece_kit_1, kit.piece_kit_2, kit.piece_kit_3, kit.piece_kit_4, kit.piece_kit_5,
                    kit.piece_kit_6, kit.piece_kit_7, kit.piece_kit_8, kit.piece_kit_9, kit.piece_kit_10,
                    kit.piece_kit_11, kit.piece_kit_12, kit.piece_kit_13, kit.piece_kit_14, kit.piece_kit_15]
    print(piece_instance)
    context = {'kit': kit, 'piece_instance':piece_instance}
    return render(request, 'inventory/kit_detail.html', context)


# Movement Management Section

def movement_exchange(request):
    form = MovementForm(request.POST or None)
    #items = PieceInstance.objects.all().order_by('serial_number')
    context = {
        'form': form,
        #'items': items,
    }
    if form.is_valid():
        obj = form.save(commit=False)
        # Update location of the item being replaced with the item it replaces
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
        # Save the objects
        print('is_valid')
        print(obj.item_1)
        obj.item_1.save()
        obj.item_2.save()
        # Save the movement
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, 'inventory/movement_choice.html', context)

def movement_detail(request, primary_key):
    movement = MovementExchange.objects.get(pk=primary_key)
    context = {'movement': movement}
    return render(request, 'inventory/movement_detail.html', context)

def movement_list(request):
    movements = MovementExchange.objects.order_by('date_created')
    context = {'movements': movements}
    return render(request, 'inventory/movement_list.html', context)

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
    return render(request, 'inventory/create_equivalence.html', context)

# Display a list of all the Pieces in the inventory
class EquivalenceListView(ListView):
    model = Equivalence
    paginate_by = 10
    template_name = 'inventory/equivalence_list.html'  # Template location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(EquivalenceListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['equivalence'] = Equivalence.objects.all().order_by('-id')
        return context

def equivalence_detail(request, primary_key):
    equivalence = Equivalence.objects.get(pk=primary_key)
    context = {'equivalence': equivalence}
    return render(request, 'inventory/equivalence_detail.html', context)

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
    return render(request, 'inventory/equivalence_update.html', context)

# Display a specific Piece
def show_piece_history(request, primary_key):
    piece = Piece.objects.get(pk=primary_key)
    history = piece.history.all()
    context = {'history': history, 'piece': piece}
    return render(request, 'inventory/piece_history.html', context)

# Display a specific Instance
def show_instance_history(request, primary_key):
    piece_instance = PieceInstance.objects.get(pk=primary_key)
    history = piece_instance.history.all()
    context = {'history': history, 'piece_instance': piece_instance}
    return render(request, 'inventory/instance_history.html', context)

# Display a specific Assembly
def show_assembly_history(request, primary_key):
    assembly = Kit.objects.get(pk=primary_key)
    history = assembly.history.all()
    context = {'history': history, 'assembly': assembly}
    return render(request, 'inventory/assembly_history.html', context)
