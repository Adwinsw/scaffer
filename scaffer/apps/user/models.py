import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class AuthMixin:
    @property
    def pwd_raw(self):
        raise AttributeError('Password raw is not a readable attribute')
    
    @pwd_raw.setter
    def pwd_raw(self, _pwd_raw):
        self.set_password(_pwd_raw)

    def set_password(self,raw_pwd):
        if self.can_update_for_pwd():
            self.date_pwd_last_updated = timezone.now()
            # post_user_change_password.send(self.__class__, user=self) 主要用于singal触发消息推送
            super().set_password(raw_pwd)

    def can_update_for_pwd(self):
        return True

    def reset_password(self, new_password):
        self.set_password(new_password)
        self.save()

class UserProfile(AuthMixin,AbstractUser):
    name = models.CharField(max_length=64,default='adwins',blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0.name}({0.username})'.format(self)

    class Meta:
        app_label = 'user'