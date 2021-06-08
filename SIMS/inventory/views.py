from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

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
    PieceForm,
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


def create_piece(request):
    forms = PieceForm()
    if request.method == 'POST':
        forms = PieceForm(request.POST)
        if forms.is_valid():
            part_number = forms.cleaned_data['part_number']
            manufacturer = forms.cleaned_data['manufacturer']
            website = forms.cleaned_data['website']
            piece_model = forms.cleaned_data['piece_model']
            cae_serialnumber = forms.cleaned_data['cae_serialnumber']
            description = forms.cleaned_data['description']
            documentation = forms.cleaned_data['documentation']
            item_type = forms.cleaned_data['item_type']
            item_characteristic = forms.cleaned_data['item_characteristic']
            Piece.objects.create(
                part_number=part_number,
                manufacturer=manufacturer,
                website=website,
                piece_model=piece_model,
                cae_serialnumber=cae_serialnumber,
                description=description,
                documentation=documentation,
                item_type=item_type,
                item_characteristic=item_characteristic,
            )
            return redirect('piece-list')
    context = {
        'form': forms
    }
    return render(request, 'inventory/create_piece.html', context)

class PieceCreate(CreateView):
    model = Piece
    fields = ['part_number', 'manufacturer', 'website', 'piece_model', 'cae_serialnumber', 'description', 'documentation', 'item_type', 'item_characteristic']

class PieceUpdate(UpdateView):
    model = Piece
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class PieceDelete(DeleteView):
    model = Piece
    success_url = reverse_lazy('piece')

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

    # Protection to verify we indeed have an existing piece
    def piece_detail_view(request, primary_key):
        piece = get_object_or_404(Piece, pk=primary_key)
        return render(request, 'inventory/piece_detail.html', context={'piece': piece})