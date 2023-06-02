from django.db import models

# Create your models here.

class Flow(models.Model):
    username = models.CharField(max_length=64,default='adwins',blank=True,null=True)

    class Meta:
        app_label = 'flow'
