# authentication.py
import uuid
from user.models import UserProfile
from django.utils import timezone
from django.conf import settings
from authen.models import TokenInfo
from rest_framework import authentication, exceptions
from rest_framework.authentication import TokenAuthentication

class SessionAuthentication(authentication.SessionAuthentication):
    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """

        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)

        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        try:
            self.enforce_csrf(request)
        except exceptions.AuthenticationFailed:
            return None

        if not CustomTokenAuthentication().authenticate(request):
            return None

        # CSRF passed with authenticated user
        return user, None

class CustomTokenAuthentication(TokenAuthentication):    
    def authenticate(self, request):
        key = request.META.get('HTTP_X_TOKEN')
        try:
            token = TokenInfo.objects.get(key=key)
        except TokenInfo.DoesNotExist:
            return None
        
        if timezone.now() > token.expired:
            TokenInfo.objects.filter(key=key).delete()
            return None
        else:
            exp_time = timezone.now()+timezone.timedelta(seconds=settings.SESSION_COOKIE_AGE)
            TokenInfo.objects.filter(key=key).update(expired=exp_time)
        if not token.user.is_active:
            return None

        return (token.user, token)
    
    def generate_token(self, user):
        token = str(uuid.uuid4())
        exp_time = timezone.now()+timezone.timedelta(seconds=settings.SESSION_COOKIE_AGE)
        if settings.ALLLOGIN_MUILTI:
            TokenInfo.objects.create(user=user, key=token, expired=exp_time)
        else:
            TokenInfo.objects.filter(user=user).delete()
            TokenInfo.objects.create(user=user, key=token, expired=exp_time)
        return token
    
    def authenticate_token(self, request):
        token = request.META.get('HTTP_X_TOKEN')
        try:
            token_user = TokenInfo.objects.get(key=token)
        except TokenInfo.DoesNotExist:
            return None
        
        if timezone.now() > token_user.expired:
            return None
        if not token_user.user.is_active:
            return None

        return token_user.user
    
    def authenticate_request(self,request, username='', password='', **kwargs):
        user = UserProfile.objects.filter(username=username).first()
        if user and user.check_password(password):
            return user

    def authenticate_refresh(self, key):
        try:
            token = TokenInfo.objects.get(key=key)
        except TokenInfo.DoesNotExist:
            return None

        new_token = str(uuid.uuid4())
        token.key = new_token
        token.save()

        return new_token
    
    def authenticate_delete(self,request):
        key = request.META.get('HTTP_X_TOKEN')
        try:
            token = TokenInfo.objects.get(key=key)
        except TokenInfo.DoesNotExist:
            return True
        else:            
            token.delete()
            return True      



