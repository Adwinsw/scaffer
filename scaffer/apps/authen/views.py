from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from authen.backends.status import CustomTokenAuthentication, SessionAuthentication
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
class LoginView(APIView):
    authentication_classes = []
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
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)  # 将用户信息保存到 Session 中
                    token = CustomTokenAuthentication().generate_token(user) 
                    return Response({'code': 20000, 'message': '登录成功！','token': token}, status=status.HTTP_200_OK)
                else:
                    return Response({'code': 40001, 'message': '信息验证失败！','token': ''}, status=status.HTTP_200_OK)
            else:
                return Response({'code': 40001, 'message': '信息验证失败！','token': ''}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'code': 40001, 'message': '登录失败，{0}'.format(ex),'token': ''}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [SessionAuthentication, CustomTokenAuthentication]
    permission_classes = []

    def post(self,request):
        try:
            auth_logout(request)
            CustomTokenAuthentication().authenticate_delete(request)
            return Response({'code': 20000, 'message': '退出登录！'}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'code': 40001, 'message': '退出登陆失败，{0}'.format(ex),'token': ''}, status=status.HTTP_200_OK)