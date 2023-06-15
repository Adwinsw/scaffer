from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name='组名称')
    create_time = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=256,default='',blank=True,null=True,verbose_name='备注')

    class Meta:
        app_label = 'user'

    @classmethod
    def initial(cls):
        default_group = cls.objects.filter(name='Default')
        if not default_group:
            group = cls(name='Default',  comment='默认组')
            group.save()
        else:
            group = default_group[0]
        return group

class AuthMixin:
    @property
    def groups_display(self):
        return ' '.join([group.name for group in self.groups.all()])

    @property
    def pwd_raw(self):
        raise AttributeError('Password raw不是一个可读属性,请去除')
    
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
    name = models.CharField(max_length=64,default='adwins',blank=True,null=True,verbose_name='用户名称')
    role_ac = models.CharField(max_length=64,default='admin',blank=True,null=True,verbose_name='角色')
    authip = models.CharField(max_length=256,default='all',blank=True,null=True,verbose_name='可信主机')
    create_time = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(UserGroup, related_name='user', blank=True, verbose_name='用户组')

    def __str__(self):
        return '{0.name}({0.username})'.format(self)

    class Meta:
        app_label = 'user'

    @classmethod
    def initial(cls):
        default_user = cls.objects.filter(username='admin')
        if not default_user:
            user = cls(name='admin',
                    username='admin',
                    role_ac='admin',
                    is_active=True,
                    is_staff=False,
                    authip='all',
                    pwd_raw='htgk@1234')
            user.save()
            user.groups.add(UserGroup.initial())
        else:
            default_user.get().groups.add(UserGroup.initial())


for cls in [UserProfile, UserGroup]:
    if hasattr(cls, 'initial'):
        cls.initial()