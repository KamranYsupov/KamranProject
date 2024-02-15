import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse


def join_room(request, current_room):
    current_room.members.add(request.user)
    current_room.last_visit = datetime.datetime.now()
    current_room.save()

    return HttpResponseRedirect(reverse('room', args=[str(current_room.id)]))

