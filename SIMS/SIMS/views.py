from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from inventory.models import Piece, PieceInstance


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects

    num_pieces = Piece.objects.all().count()
    num_instances = PieceInstance.objects.all().count()

    context = {
        'num_pieces': num_pieces,
        'num_instances': num_instances,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def dashboard(request):
    mypieces = Piece.objects.all()
    my_piece_instances = PieceInstance.objects.all().order_by('date_calibration')
    context = {
        'mypieces': mypieces,
        'my_piece_instances': my_piece_instances,
    }
    return render(request, 'dashboard.html', context=context)
