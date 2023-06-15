REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authen.backends.status.SessionAuthentication',
        'authen.backends.status.CustomTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 50
}
# POST等方法必须添加以下属性
CSRF_TRUSTED_ORIGINS = [
    'https://localhost:8080',
    'https://127.0.0.1:8080',
    'https://172.25.180.189:8080'
]