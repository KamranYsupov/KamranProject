import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from django.conf import settings
from Articles.mixins import BaseMixin
from .mixins import RoomMixin
from .forms import AddRoomForm
from .models import Room, Message

related_rooms = Room.objects.select_related('creator').prefetch_related('members')


class Rooms(RoomMixin, ListView):
    model = Room
    template_name = 'KamranGram/rooms.html'
    title = 'KamranGram'


class DetailRoom(RoomMixin, DetailView):
    model = Room
    template_name = 'KamranGram/room.html'
    context_object_name = 'room'
    pk_url_kwarg = 'room_id'

    def get_context_data(self, **kwargs):
        room = kwargs['object']
        if self.request.user not in room.members.all():
            raise forms.ValidationError(
                f'Чтобы зайти в комнату {room.name}, найдите ее в поиске и нажмите "Пресоединится"!'
            )
        messages = room.room_messages.select_related('sender')
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
    template_name = 'KamranGram/search_rooms.html'
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


@login_required
def login_room(request, room_id):
    current_room = Room.objects.get(id=room_id)
    input_password = request.POST.get('input_password')
    if current_room.members.filter(id=request.user.id):
        return HttpResponseRedirect(reverse('room', args=[str(room_id)]))
    if (input_password == current_room.password) or (not current_room.password):
        current_room.members.add(request.user)
        return HttpResponseRedirect(reverse('room', args=[str(room_id)]))

    return render(request, 'KamranGram/login_room.html', context={'room': current_room})


@login_required
def logout_room(request, room_id):
    current_room = Room.objects.get(id=room_id)
    if current_room.members.get(id=request.user.id):
        current_room.members.remove(request.user)
    return HttpResponseRedirect(reverse('rooms'))


@login_required
def delete_member(request, room_id, member_id):
    current_room = Room.objects.get(id=room_id)
    if current_room.members.get(id=member_id):
        member = current_room.members.get(id=member_id)
        current_room.members.remove(member)
    return HttpResponseRedirect(reverse('room', args=[str(room_id)]))


def update_room(request, room_id):
    current_room = Room.objects.get(id=room_id)

    current_room.is_searchable = True if request.POST.get('is_searchable') == 'on' else False
    current_room.limit_members = request.POST.get('limit_members')
    current_room.description = request.POST.get('description')
    current_room.theme = request.POST.get('theme')
    current_room.save()
    return HttpResponseRedirect(reverse('room', args=[str(room_id)]))


@login_required
def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)
    if request.user != message.sender and not request.user.is_staff:
        raise forms.ValidationError('Вы не можете удалять чужие сообщения')
    room_id = message.room.id
    message.delete()
    return HttpResponseRedirect(reverse('room', args=[str(room_id)]))


@login_required
def change_message(request, message_id):
    message = Message.objects.get(id=message_id)
    if request.user != message.sender and not request.user.is_staff:
        raise forms.ValidationError('Вы не можете изменять чужие сообщения')
    room_id = message.room.id
    if request.method == 'POST':
        message.content = request.POST.get('changed_message', 'None')
        message.is_changed = True
        message.save()
    return HttpResponseRedirect(reverse('room', args=[str(room_id)]))
