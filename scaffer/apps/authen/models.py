from django.db import models
from django.conf import settings

class TokenInfo(models.Model):
   key = models.CharField(max_length=40, primary_key=True)
   user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='auth_token', on_delete=models.CASCADE,)
   created = models.DateTimeField(auto_now_add=True)
   expired = models.DateTimeField(default=None,null=True)

   class Meta:
      app_label = 'authen'