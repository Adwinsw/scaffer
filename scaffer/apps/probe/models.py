from django.db import models

# Create your models here.

class Probe(models.Model):
    username = models.CharField(max_length=64,default='adwins',blank=True,null=True)

    class Meta:
        app_label = 'probe'