from django.db import models

# Create your models here.

class Item(models.Model):
    link = models.CharField(max_length=256)