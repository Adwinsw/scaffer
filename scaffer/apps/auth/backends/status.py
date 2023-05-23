# authentication.py
import uuid
from user.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import authentication, exceptions

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

        # CSRF passed with authenticated user
        return user, None
#用了session就不要用token
class CustomTokenAuthentication(TokenAuthentication):
    def generate_token(self, user):
        token = str(uuid.uuid4())
        Token.objects.create(user=user, key=token)
        return token

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            return None

        if not token.user.is_active:
            return None

        return (token.user, token)

    def refresh(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            return None

        new_token = str(uuid.uuid4())
        token.key = new_token
        token.save()

        return new_token

def authenticate(request, username=None, password=None, **kwargs):
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        return user
    
def get_user(user_id):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None



