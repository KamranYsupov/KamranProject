import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView

from django.conf import settings
from Articles.my_mixins import BaseMixin
from .mixins import RoomMixin
from .forms import AddRoomForm
from .models import Room, Message

related_rooms = Room.objects.select_related('creator').prefetch_related('members')


class Rooms(RoomMixin, ListView):
    template_name = 'KamranGram/rooms.html'
    title = 'KamranGram'
    model = Room
    context_object_name = 'rooms'


class DetailRoom(RoomMixin, DetailView):
    template_name = 'KamranGram/room.html'
    model = Room
    context_object_name = 'room'
    pk_url_kwarg = 'room_id'

    def get_context_data(self, **kwargs):
        room = kwargs['object']
        room.last_visit = datetime.datetime.now()
        room.save()
        messages = Message.objects.select_related('sender', 'room').filter(room=room)
        context = super().get_context_data(**kwargs)
        context['messages'] = messages
        return context


class CreateRoom(BaseMixin, CreateView):
    form_class = AddRoomForm
    template_name = 'KamranGram/create_room.html'
    success_url = reverse_lazy('rooms')
    title = 'Создание комнаты'

    def form_valid(self, form):
        f = form.save()
        f.members.add(self.request.user)
        f.creator = self.request.user
        return super().form_valid(form)


class RoomSearch(BaseMixin, LoginRequiredMixin, ListView):
    model = Room
    template_name = 'KamranGram/rooms.html'
    title = 'KamranGram'

    def get_context_data(self, *, object_list=None, **kwargs):
        query = self.request.GET.get('room_search')
        context = super().get_context_data(**kwargs)
        context['room_search'] = query
        context['rooms'] = Room.objects.filter(
            Q(name__iregex=query) |
            Q(description__iregex=query) |
            Q(creator__username__iregex=query) |
            Q(creator__first_name__iregex=query) |
            Q(creator__last_name__iregex=query)
        )
        return context


def join_room(request, room_id):
    current_room = Room.objects.get(id=room_id)
    if not current_room.members.filter(id=request.user.id):
        current_room.members.add(request.user)
    current_room.last_visit = datetime.datetime.now()
    current_room.save()
    return HttpResponseRedirect(reverse('room', args=[str(room_id)]))
