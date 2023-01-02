from django.shortcuts import render

# Create your views here.


from rest_framework.generics import ListAPIView, CreateAPIView
from .models import ReleaseApp
from .serializers import ReleaseAppModelSerializer


# Create your views here.
class ReleaseAPIView(ListAPIView, CreateAPIView):
    queryset = ReleaseApp.objects.all()
    serializer_class = ReleaseAppModelSerializer

    # 在添加数据时，补充当前用户到发布应用中。
    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        print(request.data)
        return super().create(request, *args, **kwargs)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import ReleaseRecord, ReleaseRecordDetail
import logging

logger = logging.getLogger("django")


class NewReleaseAPIView(APIView):
    def post(self, request):
        print('新建发布的数据： ', request.data)
        # 按理来讲，应该对数据进行校验，我这里就不做了，直接保存
        # 默认发布状态为待审核
        data = request.data
        # 发布应用的主机列表
        host_ids = data.pop('pub_target_host_choose')

        # 事务，在数据库中，为了保证多条SQL在同一个函数或功能中，要么一起操作成功，要么一起操作失败而提供的。
        # 关于事务在MySQL等关系型数据库中一个比较重要的概念，所以大家去看下 事务的特性：
        # 4个特性(ACID)：原子性，一致性，隔离性和持久性
        # 5个级别：指代的就是项目运行过程中，遇到多个事务一并执行的情况下，事务操作的数据之间的存在的隔离性问题,从低到高：
        # 没有隔离级别
        # 未提交读[read-uncommitted]
        # 不可重复读[read-committed]
        # 已提交读[repeatable-read]
        # 串行化[serializable]

        # 由于有两张表的数据要同时保存，所以我们要开启事务[transaction]
        with transaction.atomic():
            sid = transaction.savepoint()  # 创建事务回滚点
            try:
                re_record_obj = ReleaseRecord.objects.create(**data)
                for host_id in host_ids:
                    ReleaseRecordDetail.objects.create(
                        record_id=re_record_obj.id,
                        hosts_id=host_id
                    )
            except Exception as e:
                transaction.savepoint_rollback(sid)
                # 记录日志
                error_msg = f'新建发布失败，请联系管理员,错误信息为{str(e)}'
                logger.error(error_msg)
                # 回复错误信息提示客户端
                return Response({'error': error_msg}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({'msg': 'ok'})


'''
新建发布的数据： 
{
	'release_app_id': 1, 发布从属的应用id
	'envs_id': 1, 发布环境
	'code_git_addr': 'git@gitee.com:s32-private-club/spa.git', git仓库的ssh地址
	'msg_notice_status': True,#消息通知状态是否开启，True表示开启
	'msg_type': 1,#消息通知类型（钉钉、短信等）
	'msg_content': 消息通知内容
	#  'release_status': 1, #发布状态  这个放到发布申请的表中了
	'target_host_pub_path': '/var/www/html', 代码发布到目标主机的路径
	'target_host_repository_path': '/data/hippo/repos', 代码版本管理目录
	'keep_history_count': '10', 代码版本存储个数
	'pub_target_host_choose': [11, 10], 目标主机的id列表
	'filefilterway': 1,  # 文件过滤方式 1表示包含，2表示过滤
	'file_filter_cmd_content': 'readme.txt\nreadme.md', 代码文件过滤的指令
	'before_code_check_out_value': 'mkdir xxx', 代码检出前的执行指令
	'before_release_content': 'mkdir kkk', 代码发布前的执行指令
	'custom_global_variable': "user='root'\npassword='123'", 代码所需的全局变量
	'after_code_check_out_value': 'mkdir ooo', 代码检出后执行的指令
	'after_release_value': 'mkdir vvv' 代码发布后执行的指令
}
'''
from .serializers import ReleaseApplyModelSerializer
from rest_framework.permissions import IsAuthenticated
from . import models
from rest_framework.viewsets import ModelViewSet


# class ReleaseApplyViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = models.ReleaseApply.objects.filter(is_show=True, is_deleted=False)
#     serializer_class = ReleaseApplyModelSerializer
#

# 获取发布申请的状态数据
class ReleaseApplyStatus(APIView):
    def get(self, request):
        status = models.ReleaseApply.release_status_choices
        return Response({'status_data': status})


# 获取不同环境下的应用数据
class EnvsAppsView(APIView):

    def get(self, request):
        # 获取环境id
        envs_id = request.query_params.get('envs_id')
        envs_apps_data = list(models.ReleaseRecord.objects.filter(envs_id=envs_id).values(
            'release_app__id',
            'release_app__name',
        ).distinct())  # 别忘了去重
        return Response({'envs_apps_data': envs_apps_data})


from django.conf import settings
from .utils.git_oprations import get_git_branchs, get_git_commits


class GitBranchAPIView(APIView):
    # 获取git仓库的分支记录获取tag标签
    def get(self, request):
        app_id = request.query_params.get('app_id')
        # 先找到该应用的新建的最新发布记录
        release_record_obj = ReleaseRecord.objects.filter(is_show=True, is_deleted=False,
                                                          release_app_id=app_id).order_by('-id').first()
        git_code_dir = settings.GIT_CODE_DIR
        git_remote_attr = release_record_obj.code_git_addr
        # 获取git仓库的分支数据
        git_branch_list = get_git_branchs(git_remote_attr, git_code_dir)
        # 获得branch -- master等分支的所有提交版本
        branchs_name = request.query_params.get('branchs')  # master or dev

        commits = get_git_commits(branchs_name, git_remote_attr, git_code_dir)

        return Response({
            'branch_list': git_branch_list,
            'commits': commits,
            'release_record_id': release_record_obj.id
        })


from .serializers import ReleaseApplyModelSerializer
from rest_framework.viewsets import ModelViewSet
from .models import ReleaseApply
from rest_framework.permissions import IsAuthenticated


class ReleaseApplyViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ReleaseApply.objects.filter(is_show=True, is_deleted=False).order_by("-id")
    serializer_class = ReleaseApplyModelSerializer
