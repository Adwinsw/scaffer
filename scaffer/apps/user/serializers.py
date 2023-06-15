from rest_framework import serializers
from user.models import UserProfile, UserGroup

class UserSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        _pwd = attrs.pop('password',None)
        if _pwd and _pwd != '':
            attrs['pwd_raw'] = _pwd
        return attrs

    class Meta:
        model = UserProfile
        fields = ['id','username','name','password','create_time','authip','is_active','is_staff','role_ac','groups','groups_display']

class GroupSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects, label='用户',)

    class Meta :
        model = UserGroup
        fields = ['id','name','comment','create_time','users']