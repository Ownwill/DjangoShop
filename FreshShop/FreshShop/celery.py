import os
from celery import Celery
from django.conf import settings

#设置celery的执行环境变量，执行django项目的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE','CeleryTask.settings')

#创建celery应用
app = Celery('art_project')   #应用的名称
app.config_from_object('django.conf:settings')  #加载的配置文件

#在过程中创建tasks.py模块，那么Celery应用就会自动去检索创建的任务
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)


