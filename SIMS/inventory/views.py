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
    Kit,
)

from .forms import (
    PieceForm,
    PieceKitFormSet,
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
    instances = Piece.objects.all().order_by('part_number')

    # Add column headings to the csv file
    writer.writerow(['Manufacturer', 'Manufacturer part Number', 'Manufacturer Serial Number', 'Website', 'Description',
                     'Documentation', 'Recurrence de calibration', 'Type', 'Characteristic', 'Owner', 'Restriction',
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
        writer.writerow([instance.manufacturer, instance.part_number, instance.manufacturer_serialnumber, instance.website, instance.description, instance.documentation, instance.calibration_recurrence,
                         instance.item_type, instance.item_characteristic, instance.owner, instance.restriction, instance.kit, instance.cae_serial_number, instance.provider, instance.provider_serialnumber,
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
            return render(request, 'inventory/formset.html', {'formset': formset})

        self.object = None
        form_class = self.get_form_class()
        form = PieceForm(request.POST, request.FILES)
        if form.is_valid() :
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
    context = {'piece': piece}
    return render(request, 'inventory/piece_detail.html', context)


# Update a piece
def update_piece(request, piece_id):
    piece = Piece.objects.get(pk=piece_id)
    piece.date_update = timezone.now()
    if request.method == "POST":
        form = PieceForm(request.POST, instance=piece)
        if form.is_valid():
            form.save()
            return redirect('piece')
    else:
        form = PieceForm(instance=piece)
    context = {'piece': piece, 'form':form}
    return render(request, 'inventory/update_piece_instance.html', context)

# clone a piece
def clone_piece(request, piece_id):
    piece = Piece.objects.get(pk=piece_id)
    piece.pk=None
    piece.date_update = timezone.now()
    if request.method == "POST":
        form = PieceForm(request.POST, instance=piece)
        if form.is_valid():
            form.save()
            return redirect('piece')
    else:
        form = PieceForm(instance=piece)
    context = {'piece': piece, 'form':form}
    return render(request, 'inventory/clone_existing_piece.html', context)

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
        piece_form = PieceKitFormSet()
        context = {
            'form': KitForm(),
            'formset': PieceKitFormSet(),
        }
        return render(request, 'inventory/kit_form.html', context)

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        piece_form = PieceKitFormSet(request.POST)
        if form.is_valid() and piece_form.is_valid() :
            return self.form_valid(form, piece_form)
        else:
            return self.form_invalid(form, piece_form)

    def form_valid(self, form, piece_form):
        self.object = form.save()
        piece_form.instance = self.object
        piece_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, piece_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  piece_form=piece_form))


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
    piece = Piece.objects.all().order_by('status')
    context = {'kit': kit, 'piece': piece}
    return render(request, 'inventory/kit_detail.html', context)
