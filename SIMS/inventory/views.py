from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

from users.models import User

from .models import (
    MainUser,
    LambdaUser,
    Category,
    Location,
    Piece,
    PieceInstance
)

from .forms import (
    MainUserForm,
    LambdaUserForm,
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

class PieceListView(ListView):
    model = Piece
    paginate_by = 10

    def get_queryset(self):
        return Piece.objects.filter(owner__icontains='CAE')[:5] # Get 5 pieces containing the owner CAE

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PieceListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

    template_name = 'inventory/piece_list.html'  # Template location

class PieceDetailView(DetailView):
    model = Piece

    # Protection to verify we indeed have an existing piece
    def piece_detail_view(request, primary_key):
        piece = get_object_or_404(Piece, pk=primary_key)
        return render(request, 'inventory/piece_detail.html', context={'piece': piece})

class CategoryListView(ListView):
    model = Category
    paginate_by = 10

    def get_queryset(self):
        return Category.objects.filter(manufacturer__icontains='')[:10] # Get 5 categories

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(CategoryListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

    template_name = 'inventory/category_list.html'  # Template location


class CategoryDetailView(DetailView):
    model = Category

    # Protection to verify we indeed have an existing piece
    def category_detail_view(request, primary_key):
        category = get_object_or_404(Category, pk=primary_key)
        return render(request, 'inventory/category_detail.html', context={'category': category})