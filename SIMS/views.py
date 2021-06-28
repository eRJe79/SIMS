from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from inventory.models import MainUser, LambdaUser, Article, Item


@login_required(login_url='login')
def dashboard(request):
    #total_mainuser = MainUser.objects.count()
    #total_lambdauser = LambdaUser.objects.count()
    articles = Article.objects.all().order_by('-id')
    items = Item.objects.all().order_by('-id')
    context = {
        #'mainusers': total_mainuser,
        #'lambdausers': total_lambdauser,
        'articles': articles,
        'items': items
    }
    return render(request, 'dashboard.html', context)
