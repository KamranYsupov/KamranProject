import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from django.conf import settings
from Articles.my_mixins import BaseMixin
from .mixins import RoomMixin
from .forms import AddRoomForm
from .models import Room, Message
from .service import join_room

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
        if self.request.user not in room.members.all():
            raise forms.ValidationError(
                f'Чтобы зайти в комнату {room.name}, найдите ее в поиске и нажмите "Пресоединится"!'
            )
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


class RoomSearch(BaseMixin, ListView):
    model = Room
    template_name = 'KamranGram/rooms.html'
    title = 'KamranGram'

    def get_context_data(self, *, object_list=None, **kwargs):
        query = self.request.GET.get('room_search')
        context = super().get_context_data(**kwargs)
        context['room_search'] = query
        context['rooms'] = (related_rooms.filter(
            Q(is_searchable=True) &
            (Q(name__iregex=query) |
             Q(creator__username__iregex=query))))
        return context


def login_room(request, room_id):
    current_room = Room.objects.get(id=room_id)
    input_password = request.POST.get('input_password')
    if current_room.members.filter(id=request.user.id):
        return HttpResponseRedirect(reverse('room', args=[str(room_id)]))
    if not current_room.password:
        join_room(request, current_room)

    if input_password == current_room.password:
        join_room(request, current_room)

    return render(request, 'KamranGram/login_room.html', context={'room': current_room})
