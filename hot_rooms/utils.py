from datetime import datetime, timedelta
from django.utils.timezone import now, make_aware
from .models import Room, CommandeRoom

def update_room_status():
    today_datetime = now()
    rooms = Room.objects.all()

    for room in rooms:
        overlapping_commandes = CommandeRoom.objects.filter(
            idRoom=room,
            DateStart__lte=today_datetime,
            DateEnd__gte=today_datetime
        )

        room.available = not overlapping_commandes.exists()

        upcoming_commandes = CommandeRoom.objects.filter(
            idRoom=room
        ).order_by('DateStart')

        if upcoming_commandes.exists():
            current_date = today_datetime
            for commande in upcoming_commandes:
                if commande.DateStart <= current_date <= commande.DateEnd:
                    current_date = commande.DateEnd + timedelta(days=1)
                elif commande.DateStart > current_date:
                    break
            room.dateAvailable = current_date.date()
        else:
            room.dateAvailable = None

        room.save()