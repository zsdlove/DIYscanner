# -*- coding:utf-8 -*-
from celery import Celery

app = Celery('celery_config',include=['spider'],backend='redis://localhost:6379/4',broker='redis://localhost:6379/5')
# 官方推荐使用json作为消息序列化方式
app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
)