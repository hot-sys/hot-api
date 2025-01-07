from .models import Room, CommandeRoom
from datetime import timedelta
from django.utils.timezone import now

def update_room_status():
    today_datetime = now()
    today_date = today_datetime.date()
    rooms = Room.objects.all()

    for room in rooms:
        overlapping_commandes = CommandeRoom.objects.filter(
            idRoom=room,
            idStatus_id=3,
            DateStart__date__lte=today_date,
            DateEnd__date__gte=today_date
        )

        if overlapping_commandes.exists():
            room.available = False

            upcoming_commandes = CommandeRoom.objects.filter(
                idRoom=room,
                idStatus_id=3
            ).order_by('DateStart')

            current_date = today_date
            for commande in upcoming_commandes:
                if commande.DateStart.date() <= current_date <= commande.DateEnd.date():
                    current_date = commande.DateEnd.date() + timedelta(days=1)
                elif commande.DateStart.date() > current_date:
                    break
            room.dateAvailable = current_date
        else:
            room.available = True
            room.dateAvailable = None

        room.save()
