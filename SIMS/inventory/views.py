from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from users.models import User

from .models import (
    MainUser,
    LambdaUser,
    Item,
    Spare
)

from .forms import (
    MainUserForm,
    LambdaUserForm,
    # ArticleForm,
    ItemForm
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

# Article views
#@login_required(login_url='login')
#def create_article(request):
#    forms = ArticleForm()
#    if request.method == 'POST':
#        forms = ArticleForm(request.POST)
#        if forms.is_valid():
#            forms.save()
#            return redirect('article-list')
#    context = {
#        'form': forms
#    }
#    return render(request, 'inventory/create_article.html', context)


#class ArticleListView(ListView):
#    model = Article
#    template_name = 'inventory/article_list.html'
#    context_object_name = 'article'

# Item views
@login_required(login_url='login')
def create_item(request):
    forms = ItemForm()
    if request.method == 'POST':
        forms = ItemForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('item-list')
    context = {
        'form': forms
    }
    return render(request, 'inventory/create_item.html', context)


class ItemListView(ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'item'