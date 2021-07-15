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
)

from .forms import (
    PieceForm,
    PieceInstanceForm,
    PieceInstancePieceFormSet,
    PieceInstanceKitFormSet,
    KitForm,
)

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
    writer.writerow(['Manufacturer', 'Manufacturer part Number', 'Manufacturer Serial Number', 'Website', 'Description', 'Documentation', 'Recurrence de calibration', 'Type', 'Characteristic', 'Owner', 'Restriction',
                     'Kit', 'CAE Serial Number', 'Provider', 'Provider Serial Number', 'Location', 'Status'])

    # Loop Through and output
    for instance in instances:
        if instance.fifth_location:
            location = instance.location + "-" + instance.second_location + "-" + instance.third_location + "-" + instance.fourth_location + "-" + instance.fifth_location
        elif instance.fourth_location:
            location = instance.location + "-" + instance.second_location + "-" + instance.third_location + "-" + instance.fourth_location
        elif instance.third_location:
            location = instance.location + "-" + instance.second_location + "-" + instance.third_location
        else:
            location = instance.location + "-" + instance.second_location
        writer.writerow([instance.piece.manufacturer, instance.piece.part_number, instance.piece.manufacturer_serialnumber, instance.piece.website, instance.piece.description, instance.piece.documentation, instance.piece.calibration_recurrence,
                         instance.piece.item_type, instance.piece.item_characteristic, instance.piece.owner, instance.piece.restriction, instance.kit, instance.serial_number, instance.provider, instance.provider_serialnumber,
                         location, instance.status])
    return response

# Create new piece
def create_piece(request):
    forms = PieceForm()
    if request.method == 'POST':
        forms = PieceForm(request.POST)
        if forms.is_valid():
             forms.save()
        return redirect('piece')
    context = {
        'form': forms
    }
    return render(request, 'inventory/create_piece.html', context)

class PieceCreate(CreateView):
    template_name = 'inventory/create_piece.html'
    model = Piece
    form_class = PieceForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = PieceForm()
        instance_form = PieceInstancePieceFormSet()
        context = {
            'form': PieceForm(),
            'formset': PieceInstancePieceFormSet(),
        }
        return render(request, 'inventory/create_piece.html', context)

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        instance_form = PieceInstancePieceFormSet(request.POST)
        if form.is_valid() and instance_form.is_valid() :
            return self.form_valid(form, instance_form)
        else:
            return self.form_invalid(form, instance_form)

    def form_valid(self, form, instance_form):
        self.object = form.save()
        instance_form.instance = self.object
        instance_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, instance_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  instance_form=instance_form))


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
    instance_in_use = PieceInstance.objects.filter(status='U', piece=piece).count()
    instance_in_stock = PieceInstance.objects.filter(status='S', piece=piece).count()
    instance_in_refurbished = PieceInstance.objects.filter(status='Refurbishing', piece=piece).count()
    instance_in_reparation = PieceInstance.objects.filter(status='Reparation', piece=piece).count()
    context = {'piece': piece, 'piece_instance': piece_instance, 'instance_in_use': instance_in_use,
               'instance_in_stock': instance_in_stock, 'instance_in_refurbished': instance_in_refurbished,
               'instance_in_reparation': instance_in_reparation}
    return render(request, 'inventory/piece_detail.html', context)

def create_piece_instance(request):
    submitted = False
    form_class = PieceInstanceForm
    forms = form_class(request.POST or None)
    if request.method == "POST":
        forms = PieceInstanceForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('piece-instance-list')
        else:
            forms = PieceInstanceForm()
            if 'submitted' in request.GET:
                submitted = True
    context = {'form': forms}
    return render(request, 'inventory/create_instance_piece.html', context)

def all_piece_instance(request):
    piece_instance_list = PieceInstance.objects.all().order_by('piece')
    return render(request, 'inventory/piece_instance_list.html', {'piece_instance_list': piece_instance_list})

# Display specific instance information
def show_instance_form(request, primary_key):
    piece_instance = PieceInstance.objects.get(pk=primary_key)
    context = {'piece_instance': piece_instance}
    return render(request, 'inventory/piece_instance_detail.html', context)

# Update an instance
def update_instance(request, instance_id):
    piece_instance = PieceInstance.objects.get(pk=instance_id)
    piece_instance.date_update = timezone.now()
    if request.method == "POST":
        form = PieceInstanceForm(request.POST, instance=piece_instance)
        if form.is_valid():
            form.save()
            return redirect('piece-instance-list')
    else:
        form = PieceInstanceForm(instance=piece_instance)
    context = {'piece_instance': piece_instance, 'form':form}
    return render(request, 'inventory/update_piece_instance.html', context)

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
                                    | Q(part_number__contains=searched)
                                    | Q(manufacturer_serialnumber__contains=searched)
                                    | Q(manufacturer__contains=searched)
                                    | Q(item_type__contains=searched)
                                    | Q(item_characteristic__contains=searched)
                                    )
        context = {'searched':searched, 'results':results,
                 }
        return render(request, 'inventory/search.html', context)
    else:
        return render(request,
                    'inventory/search.html',
                    {})

# Specific to instances
def search_instance_database(request):
    if request.method == "POST":
        searched = request.POST['searched']
        results = PieceInstance.objects.filter(Q(location__contains=searched)
                                    | Q(second_location__contains=searched)
                                    | Q(third_location__contains=searched)
                                    | Q(fourth_location__contains=searched)
                                    | Q(fifth_location__contains=searched)
                                    | Q(status__contains=searched)
                                    )
        context = {'searched':searched, 'results':results,
                 }
        return render(request, 'inventory/search_instance.html', context)
    else:
        return render(request,
                    'inventory/search_instance.html',
                    {})

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
        instance_form = PieceInstanceKitFormSet()
        context = {
            'form': KitForm(),
            'formset': PieceInstanceKitFormSet(),
        }
        return render(request, 'inventory/kit_form.html', context)

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        instance_form = PieceInstanceKitFormSet(request.POST)
        if form.is_valid() and instance_form.is_valid() :
            return self.form_valid(form, instance_form)
        else:
            return self.form_invalid(form, instance_form)

    def form_valid(self, form, instance_form):
        self.object = form.save()
        instance_form.instance = self.object
        instance_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, instance_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  instance_form=instance_form))


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
