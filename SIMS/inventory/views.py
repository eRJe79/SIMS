from django.db import transaction
from django.http import Http404, HttpResponseRedirect
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
    PieceInstanceFormSet,
    KitForm,
)

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
def create_kit(request):
    forms = KitForm()
    if request.method == 'POST':
        forms = KitForm(request.POST)
        if forms.is_valid():
             forms.save()
        return redirect('piece')
    context = {
        'form': forms
    }
    return render(request, 'inventory/create_kit.html', context)

class KitCreate(CreateView):
    def get(self, request, *args, **kwargs):
        context = {
            'form': KitForm(),  # form used to create Kit instance(s)
            'formset': PieceInstanceFormSet(),  # formset for create PieceInstance instance(s) linked to a specific Kit
        }
        return render(request, 'inventory/kit_form.html', context)


def post(self, request, *args, **kwargs):
    # if our ajax is calling so we have to take action
    # because this is not the form submission
    if request.is_ajax():
        cp = request.POST.copy()  # because we couldn't change fields values directly in request.POST
        value = int(cp['wtd'])  # figure out if the process is addition or deletion
        prefix = "fk_reverse"  # whatever your related_name is
        cp[f'{prefix}-TOTAL_FORMS'] = int(
            cp[f'{prefix}-TOTAL_FORMS']) + value
        formset = PieceInstanceFormSet(cp)  # catch any data which were in the previous formsets and deliver to-
        # the new formsets again -> if the process is addition!
        return render(request, 'inventory/formset.html', {'formset': formset})
    form = KitForm(request.POST)
    formset = PieceInstanceFormSet(request.POST or None)
    theres_no_error = True
    # important note: check any desired validation of formset here and it's helpful
    # to prevent save Kit instance if formset contains invalid data which-
    # means connected PieceInstance instance(s) wont be created
    if formset.is_valid():
        for subform in formset:
            if subform.cleaned_data['name']:
                theres_no_error = False
                subform.full_clean()
                subform.errors['name'] = subform.error_class(["No name was entered"])
    if form.is_valid() and theres_no_error:  # if formsets are valid too!
        form.save()
        for subform in formset:
            subform.save()
