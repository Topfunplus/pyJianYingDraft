from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'pyJianYingDraft Django API',
        'version': '2.0.0'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health'),
    path('api/', include('api.urls')),
    path('api/auth/', include('users.urls')),
    path('', include('api.urls')),  # 首页重定向到API
]
