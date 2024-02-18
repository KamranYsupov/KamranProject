from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic.base import ContextMixin

from Articles.my_mixins import BaseMixin
from KamranGram.models import Room


class RoomMixin(BaseMixin, ContextMixin, LoginRequiredMixin):
    def __init__(self):
        super().__init__()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.prefetch_related('members').filter(members=self.request.user)
        context['KamranGram'] = True

        return context
