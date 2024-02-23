from django.contrib.auth import get_user_model
from django.views.generic import DetailView

from Articles.mixins import BaseMixin
from .models import User


class ChannelMixin(BaseMixin, DetailView):
    queryset = get_user_model().objects.prefetch_related('followers')
    context_object_name = 'object'
    pk_url_kwarg = 'owner_id'
    template_name = None
    order = None

    def __init__(self):
        super().__init__()
        if self.order:
            self.extra_context['order'] = self.order

    def get_context_data(self, **kwargs):
        owner = kwargs['object']
        context = super().get_context_data(**kwargs)
        context['owner'] = owner
        return context


class ArticlesChannelMixin(ChannelMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['followed_by'] = context['owner'].followed_by.all()[:10]
        context['followers'] = context['owner'].followers.all()[:10]
        return context
