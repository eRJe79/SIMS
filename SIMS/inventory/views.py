import csv

from django.db import transaction
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from simple_history.utils import update_change_reason
from django.template import RequestContext
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
)

from .forms import (
    PieceForm,
    PieceInstanceForm,
    PieceInstancePieceFormSet,
    PieceInstanceKitFormSet,
    KitForm,
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
    sixth_loc = Sixth_location.objects.filter(fifth_loc_id=fifth_loc_id).order_by('name')
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
    instance_in_use = PieceInstance.objects.filter(status='Use', piece=piece).count()
    instance_in_stock = PieceInstance.objects.filter(status='Stock', piece=piece).count()
    instance_in_refurbished = PieceInstance.objects.filter(status='Refurbishing', piece=piece).count()
    instance_in_reparation = PieceInstance.objects.filter(status='Reparation', piece=piece).count()
    context = {'piece': piece, 'piece_instance': piece_instance, 'instance_in_use': instance_in_use,
               'instance_in_stock': instance_in_stock, 'instance_in_refurbished': instance_in_refurbished,
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
    piece_instance.pk=None
    piece_instance.update_comment = ''
    if request.method == "POST":
        form = PieceInstanceForm(request.POST, request.FILES, instance=piece_instance)
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
            results = PieceInstance.objects.filter(Q(location__contains=searched)
                                                   | Q(second_location__contains=searched)
                                                   | Q(third_location__contains=searched)
                                                   | Q(fourth_location__contains=searched)
                                                   | Q(fifth_location__contains=searched)
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

# Kit Management Section
# Create new kit
class KitCreate(CreateView):
    template_name = 'inventory/kit_form.html'
    model = Kit
    form_class = KitForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = KitForm()
        context = {
            'form': KitForm(),
        }
        return render(request, 'inventory/kit_form.html', context)

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid() :
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


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
