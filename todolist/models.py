from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=256)
    details = models.TextField(blank=True, null=True, help_text='Detailed Description of the item.')
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

