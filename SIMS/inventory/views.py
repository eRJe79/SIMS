from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.utils.translation import ugettext as _
from django.db.models import Q


from .models import (
    Piece,
    PieceInstance
)

from .forms import (
    PieceForm,
    PieceInstanceForm,
)

# Search feature
# Specific to piece
def search_piece_database(request):
    if request.method == "POST":
        searched = request.POST['searched']
        results = Piece.objects.filter(Q(piece_model__contains=searched)
                                    | Q(part_number__contains=searched)
                                    | Q(cae_serialnumber__contains=searched)
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
                                    | Q(status__contains=searched)
                                    )
        context = {'searched':searched, 'results':results,
                 }
        return render(request, 'inventory/search_instance.html', context)
    else:
        return render(request,
                    'inventory/search_instance.html',
                    {})

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
    return render(request, 'inventory/piece_detail.html',
                  context)

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
            forms = PieceInstanceForm
            if 'submitted' in request.GET:
                submitted = True
    context = {'form': forms}
    return render(request, 'inventory/create_instance_piece.html', context)

def all_piece_instance(request):
    piece_instance_list = PieceInstance.objects.all().order_by('piece')

    return render(request, 'inventory/piece_instance_list.html', {'piece_instance_list': piece_instance_list})

class PieceCreate(CreateView):
    model = Piece
    fields = ['part_number', 'manufacturer', 'website', 'piece_model', 'cae_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic', 'owner', 'restriction']

class PieceUpdate(UpdateView):
    model = Piece
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class PieceInstanceUpdate(UpdateView):
    model = PieceInstance
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class PieceDelete(DeleteView):
    model = Piece
    success_url = reverse_lazy('piece')

class PieceInstanceDelete(DeleteView):
    model = PieceInstance
    success_url = "/"

def show_instance_form(request):
    model = PieceInstance
    inventory = PieceInstance.objects.all()
    if request.method == "POST":
        form = PieceInstanceForm(data=request.POST)
        if form.is_valid():
            form.save()
            print('valid form')
    else:
        print('unvalid form')
        form = PieceInstanceForm()
        context = {
            'form': form, 'inventory': inventory,
        }
    return render(request, 'inventory/piece_instance_detail.html', context)

def delete_instance(request):
    if request.method == 'POST':
        form = PieceInstanceForm()
        inventory = PieceInstance.objects.all()
        piece_instance_id = str(request.POST.get('piece_instance_id'))
        piece_instance = PieceInstance.objects.get(id=piece_instance_id)
        piece_instance.delete()
        context = {
            'form': form, 'inventory': inventory,
        }
        return render(request, 'inventory/piece_instance_detail.html', context)


class PieceListView(ListView):
    model = Piece
    paginate_by = 10
    template_name = 'inventory/piece_list.html'  # Template location

    #def get_queryset(self):
        #return Piece.objects.filter(piece_model__icontains='carte')[:1] # Get 5 pieces containing the model 'carte'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PieceListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['piece'] = Piece.objects.all().order_by('-id')
        return context

class SearchView(ListView):
    model = Piece
    template_name = 'search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
       result = super(SearchView, self).get_queryset()
       query = self.request.GET.get('search')
       if query:
          postresult = Piece.objects.filter(title__contains=query)
          result = postresult
       else:
           result = None
       return result

class PieceInstanceInline(InlineFormSetFactory):
    model = PieceInstance
    fields = ['piece', 'instance_number', 'location', 'status']


class PieceDetailView(DetailView):
    model = Piece
    extra_context = {
        'object_name': _(u'Piece'),
    }

    # Protection to verify we indeed have an existing piece
    def piece_detail_view(request, primary_key):
        mypiece = get_object_or_404(Piece, pk=primary_key)
        context = {'piece': mypiece}
        return render(request, 'inventory/piece_detail.html', context)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PieceDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['piece_instance'] = PieceInstance.objects.all().order_by('status')
        return context


class PieceInline(InlineFormSetFactory):
    model = Piece
    fields = ['part_number', 'manufacturer', 'website', 'piece_model', 'cae_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic', 'owner', 'restriction']


class CreatePieceView(CreateWithInlinesView):
    model = Piece
    inlines = [PieceInstanceInline]
    fields = ['part_number', 'manufacturer', 'website', 'piece_model', 'cae_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic', 'owner', 'restriction']
    #template_name = 'inventory/create_instance_piece.html'  # Template location

    def get_success_url(self):
        return self.object.get_absolute_url()

class UpdateCreatePieceView(UpdateView):
    model = Piece

    def piece_update_view(request, primary_key):
        piece = get_object_or_404(Piece, pk=primary_key)
        return render(request, 'inventory/update_piece.html', context={'piece': piece})
