import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView


class BaseMixin:
    login_url = reverse_lazy('session_login')

    title = None
    current_date = datetime.datetime.now()
    extra_context = {}

    def __init__(self):
        if self.title:
            self.extra_context['title'] = self.title
        if self.current_date:
            self.extra_context['current_date'] = self.current_date


class ArticlesMixin(BaseMixin, ListView):
    paginate_by = 5
    queryset = None
    context_object_name = 'posts'
    template_name = 'articles/list_of_pages.html'
    title = 'Новости'
    order = None

    def __init__(self):
        super().__init__()
        if self.order:
            self.extra_context['order'] = self.order
