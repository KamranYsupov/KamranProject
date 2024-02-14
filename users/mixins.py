from django.contrib.auth import get_user_model
from django.views.generic import DetailView

from Articles.my_mixins import BaseMixin
from .models import User


class ChannelMixin(BaseMixin, DetailView):
    queryset = get_user_model().objects.prefetch_related('followers')
    template_name = None
    context_object_name = 'object'
    pk_url_kwarg = 'owner_id'

    def get_context_data(self, **kwargs):
        owner = kwargs['object']
        context = super().get_context_data(**kwargs)
        context['owner'] = owner
        return context
