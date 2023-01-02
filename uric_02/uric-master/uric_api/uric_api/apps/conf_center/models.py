from django.db import models

# Create your models here.
from uric_api.utils.models import BaseModel,models
# Create your models here.
class Environment(BaseModel):
    tag = models.CharField(max_length=32,verbose_name='标识符')
    class Meta:
        db_table = "environment"  # Ctrl+Shift+U 把选中的内容进行大小写切换
        verbose_name = "环境配置"
        verbose_name_plural = verbose_name