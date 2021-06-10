from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.utils.translation import ugettext as _

from users.models import User

from .models import (
    MainUser,
    LambdaUser,
    Piece,
    PieceInstance
)

from .forms import (
    MainUserForm,
    LambdaUserForm,
    PieceInstanceForm,
)

# Main User views
@login_required(login_url='login')
def create_mainuser(request):
    forms = MainUserForm()
    if request.method == 'POST':
        forms = MainUserForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(
                    username=username, password=password,
                    email=email, is_main_user=True
                )
                MainUser.objects.create(user=user, name=name, address=address)
                return redirect('mainuser-list')
    context = {
        'form': forms
    }
    return render(request, 'inventory/create_mainuser.html', context)

class MainUserListView(ListView):
    model = MainUser
    template_name = 'inventory/mainuser_list.html'
    context_object_name = 'mainuser'

# Read-only account views
@login_required(login_url='login')
def create_lambdauser(request):
    forms = LambdaUserForm()
    if request.method == 'POST':
        forms = LambdaUserForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(
                    username=username, password=password,
                    email=email, is_lambda=True
                )
                LambdaUser.objects.create(user=user, name=name, address=address)
                return redirect('lambdauser-list')
    context = {
        'form': forms
    }
    return render(request, 'inventory/create_lambdauser.html', context)

class LambdaUserListView(ListView):
    model = LambdaUser
    template_name = 'inventory/lambdauser_list.html'
    context_object_name = 'lambdauser'


class PieceCreate(CreateView):
    model = Piece
    fields = ['part_number', 'manufacturer', 'website', 'piece_model', 'cae_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic']


class PieceUpdate(UpdateView):
    model = Piece
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class PieceDelete(DeleteView):
    model = Piece
    success_url = reverse_lazy('piece')

class PieceInstanceDelete(DeleteView):
    model = PieceInstance
    success_url = "/"


# def delete_view(request, *args, **kwargs):
#     # dictionary for initial data with
#     # field names as keys
#     context = {}
#
#     # fetch the object related to passed id
#     obj = get_object_or_404(PieceInstance, pk=kwargs.__str__())
#
#     if request.method == "POST":
#         # delete object
#         obj.delete()
#         # after deleting redirect to
#         # home page
#         return HttpResponseRedirect("/")
#
#     return render(request, "inventory/delete_view.html", context)

def show_instance_form(request):
    model = PieceInstance
    inventory = PieceInstance.objects.all()
    if request.method == "POST":
        form = PieceInstanceForm(data = request.POST)
        if form.is_valid():
            form.save()
    else:
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


class PieceDetailView(DetailView):
    model = Piece
    extra_context = {
        'object_name': _(u'Piece'),
    }
    # Protection to verify we indeed have an existing piece
    def piece_detail_view(request, primary_key):
        piece = get_object_or_404(Piece, pk=primary_key)
        return render(request, 'inventory/piece_detail.html', context={'piece': piece})

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PieceDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['piece_instance'] = PieceInstance.objects.all().order_by('-id')
        return context


class PieceInstanceInline(InlineFormSetFactory):
    model = PieceInstance
    fields = ['piece', 'instance_number', 'location', 'status', 'owner', 'restriction']

class PieceInline(InlineFormSetFactory):
    model = Piece
    fields = ['part_number', 'manufacturer', 'website', 'piece_model', 'cae_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic']

class CreatePieceView(CreateWithInlinesView):
    model = Piece
    inlines = [PieceInstanceInline]
    fields = ['part_number', 'manufacturer', 'website', 'piece_model', 'cae_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic']
    template_name = 'inventory/create_instance_piece.html'  # Template location

    def get_success_url(self):
        return self.object.get_absolute_url()

class UpdateCreatePieceView(UpdateView):
    model = Piece

    def piece_update_view(request, primary_key):
        piece = get_object_or_404(Piece, pk=primary_key)
        return render(request, 'inventory/update_piece.html', context={'piece': piece})
