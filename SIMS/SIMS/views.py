from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from inventory.models import Piece, PieceInstance


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects

    num_pieces = Piece.objects.all().count()
    num_instances = PieceInstance.objects.all().count()

    # Available books (status = 'a')
    #num_instances_available = PieceInstance.objects.filter(status__exact='S').count()

    context = {
        'num_pieces': num_pieces,
        'num_instances': num_instances,
        #'num_instances_available': num_instances_available,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
