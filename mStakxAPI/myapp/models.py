from django.db import models
from django.utils import timezone
from datetime import date
from django_mysql.models import ListCharField


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.CharField(max_length=255, blank=True, null=True)
    author = ListCharField(base_field=models.CharField(max_length=100),
                           size=6,
                           max_length=6*101)
    nopages = models.IntegerField(null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    released = models.DateField(default=timezone.now())

    class Meta:
        unique_together = (('name', 'isbn'),)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
