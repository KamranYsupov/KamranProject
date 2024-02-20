from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F, Max
from django.views.generic import ListView
from django.views.generic.base import ContextMixin

from Articles.mixins import BaseMixin
from KamranGram.models import Room


class RoomMixin(BaseMixin, LoginRequiredMixin):
    def __init__(self):
        super().__init__()

    def get_queryset(self):
        return Room.objects.select_related('creator').prefetch_related('members')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = (Room.objects
                            .select_related('creator')
                            .prefetch_related('members')
                            .filter(members=self.request.user)
                            .annotate(last_message=Max('room_messages'))
                            .order_by('-last_message')
                            )

        context['KamranGram'] = True

        return context
