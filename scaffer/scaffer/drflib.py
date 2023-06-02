REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authen.backends.status.SessionAuthentication',
        'authen.backends.status.CustomTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

CSRF_TRUSTED_ORIGINS = [
    'https://localhost:8080',
    'https://127.0.0.1:8080',
]