from .models import Piece, PieceInstance, Kit, MovementExchange, GroupAssembly, Equivalence, Consumable
import django_tables2 as tables


class PieceTable(tables.Table):
    class Meta:
        model = Piece
        sequence = ("name", "cae_part_number", "piece_model", "manufacturer", "manufacturer_part_number", "provider",
                    "provider_part_number", "item_type", "item_characteristic",)
        exclude = ("website", "description", "update_comment", "image", "calibration_recurrence", "history", "id",
                   "documentation",)
        
