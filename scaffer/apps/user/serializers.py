from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        _pwd = attrs.pop('password',None)
        if _pwd:
            attrs['pwd_raw'] = _pwd        
        return super().validate(attrs)

    class Meta:
        model = User
        fields = ['id','username','name','password','last_login']