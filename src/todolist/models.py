from django.db import models
from django.urls import reverse


# Create your models here.
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey('List', on_delete=models.RESTRICT, default=None)

    class Meta:
        unique_together = ('list', 'text')

class List(models.Model):
    def get_absolute_url(self):
        return reverse('todolist:view_list', args=[self.id])
