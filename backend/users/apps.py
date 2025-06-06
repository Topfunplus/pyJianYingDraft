from django.apps import AppConfig


# 这个类是用来 # 配置 Django 应用程序的元数据
# 比如应用程序的名称、默认的自动字段类型等
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
