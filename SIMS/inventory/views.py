import csv

from django.db import transaction
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from simple_history.utils import update_change_reason
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.utils.translation import ugettext as _
from django.db.models import Q


from .models import (
    Piece,
    PieceInstance,
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
    PieceInstanceKitFormSet,
    KitForm,
    MovementForm,
)

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
    instance_installed = PieceInstance.objects.filter(status='Installed', piece=piece).count()
    instance_in_stock = PieceInstance.objects.filter(status='In Stock', piece=piece).count()
    instance_discarded = PieceInstance.objects.filter(status='Discarded', piece=piece).count()
    instance_in_reparation = PieceInstance.objects.filter(status='In Repair', piece=piece).count()
    context = {'piece': piece, 'piece_instance': piece_instance, 'instance_installed': instance_installed,
               'instance_in_stock': instance_in_stock, 'instance_discarded': instance_discarded,
               'instance_in_reparation': instance_in_reparation}
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

def all_piece_instance(request):
    piece_instance_list = PieceInstance.objects.all().order_by('piece')
    return render(request, 'inventory/piece_instance_list.html', {'piece_instance_list': piece_instance_list})

# Display specific instance information
def show_instance_form(request, primary_key):
    piece_instance = PieceInstance.objects.get(pk=primary_key)
    context = {'piece_instance': piece_instance}
    return render(request, 'inventory/piece_instance_detail.html', context)

# Update an instance
def update_piece(request, piece_id):
    piece = Piece.objects.get(pk=piece_id)
    piece.update_comment = ''
    if request.method == "POST":
        form = PieceForm(request.POST, request.FILES, instance=piece)
        if form.is_valid():
            form.save()
            return redirect('piece')
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
            return redirect('piece')
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
            return redirect('piece-instance-list')
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
            return redirect('piece-instance-list')
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

# Assembly Management Section
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
        if request.is_ajax():
            cp = request.POST.copy()  # because we couldn't change fields values directly in request.POST
            value = int(cp['wtd'])  # figure out if the process is addition or deletion
            prefix = "instance_reverse"
            cp[f'{prefix}-TOTAL_FORMS'] = int(
                cp[f'{prefix}-TOTAL_FORMS']) + value
            formset = PieceInstanceKitFormSet(
                cp)  # catch any data which were in the previous formsets and deliver to-
            # the new formsets again -> if the process is addition!
            return render(request, 'inventory/formset.html', {'formset': formset})
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
    form = KitForm(request.POST or None, instance=kit)
    PieceInstanceFormset = modelformset_factory(PieceInstance, form=PieceInstanceForm, extra=0)
    qs = kit.pieceinstance_set.all()
    formset = PieceInstanceFormset(request.POST or None, request.FILES or None, queryset=qs)
    context = {
        'kit': kit,
        'formset': formset,
        'form': form,
    }
    if all([form.is_valid() and formset.is_valid()]):
        print("form and formset valid")
        parent = form.save(commit=False)
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            if child.serial_number is not None:
                if child.kit is None:
                    print("Added new assembly")
                    child.kit = parent
                child.update_comment = kit.update_comment
                child.first_location = kit.first_location
                child.second_location = kit.second_location
                child.third_location = kit.third_location
                child.fourth_location = kit.fourth_location
                child.fifth_location = kit.fifth_location
                child.sixth_location = kit.sixth_location
                child.seventh_location = kit.seventh_location
                child.eighth_location = kit.eighth_location
                child.status = kit.kit_status
                child.save()
        return redirect('kit-list')
    return render(request, 'inventory/kit_update.html', context)


def update_computer_assembly(request, kit_id):
    kit = Kit.objects.get(pk=kit_id)
    kit.date_update = timezone.now()
    kit.update_comment = ''
    print(kit.name)
    form = KitForm(request.POST or None, instance=kit)
    qs = kit.pieceinstance_set.all()
    # We have 1 CPU, 2 Memory Disk, 1 GPU and 1 RAM per computer = 5 components
    print(qs)
    if qs:
        ComputerFormset = modelformset_factory(PieceInstance, form=PieceInstanceForm, extra=0)
    else:
        ComputerFormset = modelformset_factory(PieceInstance, form=PieceInstanceForm, extra=5)
    formset_computer = ComputerFormset(request.POST or None, request.FILES or None, queryset=qs)
    context = {
        'kit': kit,
        'formset_computer': formset_computer,
        'form': form,
    }
    if all([form.is_valid() and formset_computer.is_valid()]):
        print("form and formsets valid")
        parent = form.save(commit=False)
        parent.save()
        for form in formset_computer:
            child = form.save(commit=False)
            print(child)
            if child.kit is None:
                print("Added new cpu")
                child.kit = parent
            child.update_comment = kit.update_comment
            child.first_location = kit.first_location
            child.second_location = kit.second_location
            child.third_location = kit.third_location
            child.fourth_location = kit.fourth_location
            child.fifth_location = kit.fifth_location
            child.sixth_location = kit.sixth_location
            child.seventh_location = kit.seventh_location
            child.eighth_location = kit.eighth_location
            child.status = kit.kit_status
            child.save()
        print(child)
        return redirect('kit-list')
    else:
        print(form.errors)
        print(formset_computer.errors)
    return render(request, 'inventory/computer_update.html', context)


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
    piece_instance = PieceInstance.objects.all().order_by('status')
    context = {'kit': kit, 'piece_instance': piece_instance}
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
        # Put object being replaced in waiting zone
        obj.item_1.first_location = First_location.objects.get(name='Waiting')
        obj.item_1.second_location = None
        obj.item_1.third_location = None
        obj.item_1.fourth_location = None
        obj.item_1.fifth_location = None
        obj.item_1.sixth_location = None
        obj.item_1.seventh_location = None
        obj.item_1.eighth_location = None
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

def mount_piece_instance(request, item_id):
    context = {}
    return render(request, 'inventory/movement_mount.html', context)

def dismount_piece_instance(request, item_id):
    context = {}
    return render(request, 'inventory/movement_dismount.html', context)

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
