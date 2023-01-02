from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#//User模型，继承Django认证系统的用户模型类，添加手机号码和用户头像两个字段
class User(AbstractUser):
    #charfield类型，最大15个字符
    mobile = models.CharField(max_length=15, unique=True, verbose_name='手机号码')
    # upload_to 表示上传文件的存储子路由，需要在settings配置中，配置上传文件的支持
    #image类型 允许为空
    avatar = models.ImageField(upload_to='avatar', verbose_name='用户头像', null=True, blank=True)
    #数据库信息
    class Meta:
        #表名
        db_table = 'uric_user'
        #详细名称
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
