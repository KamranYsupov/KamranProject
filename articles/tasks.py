import time

from celery import shared_task
from celery_singleton import Singleton
from django.db.models import Count, F
from django.db.transaction import atomic


@shared_task(base=Singleton)
def set_like_percent(article_id):
    from .models import Article

    time.sleep(10)

    with atomic():
        article = Article.objects.filter(id=article_id).annotate(annotated_percent=(Count('likes') * 100
                                                                                    / F('views'))).first()
        article.like_percent = article.annotated_percent
        article.save()


