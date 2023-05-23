from django.db import models

# Create your models here.

class Scanner(models.Model):
    username = models.CharField(max_length=64,default='adwins',blank=True,null=True)

    class Meta:
        app_label = 'scanner'