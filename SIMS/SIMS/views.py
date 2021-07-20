from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from inventory.models import Piece


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects

    num_pieces = Piece.objects.all().count()

    context = {
        'num_pieces': num_pieces,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def dashboard(request):
    mypieces = Piece.objects.all()
    context = {
        'mypieces': mypieces,
    }
    return render(request, 'dashboard.html', context=context)
