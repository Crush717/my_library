from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    应用程序配置对象：https://docs.djangoproject.com/zh-hans/4.1/ref/applications/#application-configuration
    """
    # 自动设置主键：https://docs.djangoproject.com/zh-hans/4.1/topics/db/models/#automatic-primary-key-fields
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
