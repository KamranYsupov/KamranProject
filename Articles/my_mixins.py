from django.urls import reverse_lazy
from django.views.generic import ListView

from KAMRAN import settings


class BaseMixin:
    login_url = reverse_lazy('session_login')

    default_avatar = settings.DEFAULT_AVATAR
    title = None
    extra_context = {}

    def __init__(self):
        if self.title:
            self.extra_context['title'] = self.title
        self.extra_context['default_avatar'] = self.default_avatar


class ArticlesMixin(BaseMixin, ListView):
    paginate_by = 5
    queryset = None
    context_object_name = 'posts'
    template_name = 'Articles/list_of_pages.html'
    title = 'Новости'
    order = None

    def __init__(self):
        super().__init__()
        if self.order:
            self.extra_context['order'] = self.order
