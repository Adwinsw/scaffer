from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .backends.status import CustomTokenAuthentication, authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout

# Create your views here.

class AuthView(APIView):
    permission_classes = []

    def get(self, request): 
        self.request.session.set_test_cookie()
        html = f"<html> \
                    <body> \
                        <form action='' method='post'> \
                            登录名：<input name='username' value='' /><br /> \
                            密码：<input name='password' value='' /><br /> \
                            <input type='submit' value='提交'>\
                        </form> \
                    </body> \
                </html>"
        return HttpResponse(html)
    
    def post(self, request):
        if not self.request.session.test_cookie_worked():
            return HttpResponse("Please enable cookies and try again.")
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # 将用户信息保存到 Session 中
                # token = CustomTokenAuthentication().generate_token(user) 用了session就不要用token
                return Response({'success': 'login success'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            return Response({'error': 'login failed {0}'.format(ex)}, status=status.HTTP_401_UNAUTHORIZED)