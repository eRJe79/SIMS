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
    my_piece_instances = PieceInstance.objects.all().order_by('date_calibration')# This function is to check if the FMS1/2 (second_location_) have no missing piece
    # We just check the fourth_location attribute since the specific FMS location are at this level
    fms1_number_seat=0
    fms1_number_front=0
    fms1_number_aft=0
    fms1_number_ofloor=0
    fms1_number_ufloor=0
    fms1_number_structure=0

    fms2_number_seat = 0
    fms2_number_front = 0
    fms2_number_aft = 0
    fms2_number_ofloor = 0
    fms2_number_ufloor = 0
    fms2_number_structure = 0

    for piece in my_piece_instances:
        if piece.second_location == 'FMS1':
            if piece.fourth_location == 'Seat':
                fms1_number_seat = fms1_number_seat + 1
            else:
                fms1_number_seat = fms1_number_seat
            if piece.fourth_location == 'Front':
                fms1_number_front = fms1_number_front + 1
            else:
                fms1_number_front = fms1_number_front
            if piece.fourth_location == 'Aft':
                fms1_number_aft = fms1_number_aft + 1
            else:
                fms1_number_aft = fms1_number_aft
            if piece.fourth_location == 'Over Floor':
                fms1_number_ofloor = fms1_number_ofloor + 1
            else:
                fms1_number_ofloor = fms1_number_ofloor
            if piece.fourth_location == 'Under Floor':
                fms1_number_ufloor = fms1_number_ufloor + 1
            else:
                fms1_number_ufloor = fms1_number_ufloor
            if piece.fourth_location == 'Structure':
                fms1_number_structure = fms1_number_structure + 1
            else:
                fms1_number_structure = fms1_number_structure
        elif piece.second_location == 'FMS2':
            if piece.fourth_location == 'Seat':
                fms2_number_seat = fms2_number_seat + 1
            else:
                fms2_number_seat = fms2_number_seat
            if piece.fourth_location == 'Front':
                fms2_number_front = fms2_number_front + 1
            else:
                fms2_number_front = fms2_number_front
            if piece.fourth_location == 'Aft':
                fms2_number_aft = fms2_number_aft + 1
            else:
                fms2_number_aft = fms2_number_aft
            if piece.fourth_location == 'Over Floor':
                fms2_number_ofloor = fms2_number_ofloor + 1
            else:
                fms2_number_ofloor = fms2_number_ofloor
            if piece.fourth_location == 'Under Floor':
                fms2_number_ufloor = fms2_number_ufloor + 1
            else:
                fms2_number_ufloor = fms2_number_ufloor
            if piece.fourth_location == 'Structure':
                fms2_number_structure = fms2_number_structure + 1
            else:
                fms2_number_structure = fms2_number_structure

        if fms1_number_seat > 0:
            fms1_check_seat = 'OK'
        else:
            fms1_check_seat = 'Missing'
        if fms1_number_front > 0:
            fms1_check_front = 'OK'
        else:
            fms1_check_front = 'Missing'
        if fms1_number_aft > 0:
            fms1_check_aft  = 'OK'
        else:
            fms1_check_aft  = 'Missing'
        if fms1_number_ofloor > 0:
            fms1_check_ofloor = 'OK'
        else:
            fms1_check_ofloor = 'Missing'
        if fms1_number_ufloor > 0:
            fms1_check_ufloor = 'OK'
        else:
            fms1_check_ufloor = 'Missing'
        if fms1_number_structure > 0:
            fms1_check_structure = 'OK'
        else:
            fms1_check_structure = 'Missing'

        if fms2_number_seat > 0:
            fms2_check_seat = 'OK'
        else:
            fms2_check_seat = 'Missing'
        if fms2_number_front > 0:
            fms2_check_front = 'OK'
        else:
            fms2_check_front = 'Missing'
        if fms2_number_aft > 0:
            fms2_check_aft  = 'OK'
        else:
            fms2_check_aft  = 'Missing'
        if fms2_number_ofloor > 0:
            fms2_check_ofloor = 'OK'
        else:
            fms2_check_ofloor = 'Missing'
        if fms2_number_ufloor > 0:
            fms2_check_ufloor = 'OK'
        else:
            fms2_check_ufloor = 'Missing'
        if fms1_number_structure > 0:
            fms2_check_structure = 'OK'
        else:
            fms2_check_structure = 'Missing'
    context = {
        'mypieces': mypieces,
        'my_piece_instances': my_piece_instances,
        # 'fms1_check_seat': fms1_check_seat,
        # 'fms1_check_front': fms1_check_front,
        # 'fms1_check_aft': fms1_check_aft,
        # 'fms1_check_ofloor': fms1_check_ofloor,
        # 'fms1_check_ufloor': fms1_check_ufloor,
        # 'fms1_check_structure': fms1_check_structure,
        # 'fms2_check_seat': fms2_check_seat,
        # 'fms2_check_front': fms2_check_front,
        # 'fms2_check_aft': fms2_check_aft,
        # 'fms2_check_ofloor': fms2_check_ofloor,
        # 'fms2_check_ufloor': fms2_check_ufloor,
        # 'fms2_check_structure': fms2_check_structure,
    }
    return render(request, 'dashboard.html', context=context)
