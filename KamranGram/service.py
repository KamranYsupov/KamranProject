import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse


def join_room(request, current_room):
    current_room.members.add(request.user)


