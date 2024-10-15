from django.db import models

from news_app.models import News


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.status.Published)