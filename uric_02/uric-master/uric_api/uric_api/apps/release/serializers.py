from rest_framework import serializers
from .models import ReleaseApp


class ReleaseAppModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseApp
        fields = ["id", "name", "tag", "description","user"]


from rest_framework import serializers
from release import models


# 新建发布的序列化器
class ReleaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReleaseApp
        fields = '__all__'
        extra_kwargs = {
            'remark': {
                'required': False,
                # 'allow_blank': True,
                # 'allow_null': True,
            },
            'user': {
                'required': False,
                # 'allow_blank': True,
                # 'allow_null': True,
            }

        }

    def create(self, validated_data):
        user_obj = models.ReleaseApp.objects.create(**{
            'name': validated_data.get('name'),
            'app_id': validated_data.get('app_id'),
            # 'user':self.context['request'].user.id,
            'user_id': 1,
            'remark': validated_data.get('remark'),
        })
        return user_obj


# # 新建发布申请的序列化器
# class ReleaseApplyModelSerializer(serializers.ModelSerializer):
#     app_name = serializers.CharField(source='release_record.release_app.name',read_only=True)
#     envs_name = serializers.CharField(source='release_record.envs.name',read_only=True)
#     username = serializers.CharField(source='user.username',read_only=True)
#
#     # 关于git_release_commit_id只有现在选择的是git分支时才需要传递过来进行序列化器的校验，所有我们暂时不对他进行校验，回头再补充
#
#     class Meta:
#         model = models.ReleaseApply
#         fields = ['id', 'name', 'app_name', 'envs_name', 'git_release_branch_or_tag','git_release_branch_or_tag_name', 'git_release_version', 'release_status', 'get_release_status_display', 'username', 'created_time', 'release_record', ]
#         # branch_or_tag_choices为发布申请的状态数据
#         extra_kwargs = {
#             'release_status': {'read_only': True},
#             'created_time': {'read_only': True},
#         }
#
#     # 对数据进行额外的校验
#     # def validate(self, attrs):
#     #     pass
#
#     # 自定定制create，因为保存的数据不仅仅是用提交过来的数据，并且该方法的返回值是新创建的记录的模型类对象
#     def create(self, validated_data):
#         # self.context['request'].user  用户信息
#         user_id = 1
#         new_obj = models.ReleaseApply.objects.create(**{
#             "git_release_branch_or_tag": validated_data.get('git_release_branch_or_tag'),
#             "git_release_version": validated_data.get('git_release_version'),
#             "name": validated_data.get('name'),
#             "git_release_commit_id": validated_data.get('git_release_commit_id'),
#             "description": validated_data.get('description'),
#             "release_record": validated_data.get('release_record'),
#             "user_id": user_id,
#         })
#
#         return new_obj


from .models import ReleaseApply


class ReleaseApplyModelSerializer(serializers.ModelSerializer):
    app_name = serializers.CharField(source='release_record.release_app.name', read_only=True)
    envs_name = serializers.CharField(source='release_record.envs.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    # 关于git_release_commit_id只有现在选择的是git分支时才需要传递过来进行序列化器的校验，所有我们暂时不对他进行校验，回头再补充

    class Meta:
        model = ReleaseApply
        fields = ['id', 'name', 'app_name', 'envs_name', 'git_release_branch_or_tag',
                  'git_release_branch_or_tag_name', 'git_release_version', 'release_status',
                  'get_release_status_display', 'username', 'created_time', 'release_record', 'git_release_commit_id',
                  'review_user', 'review_desc']

        # branch_or_tag_choices为发布申请的状态数据
        extra_kwargs = {
            'created_time': {'read_only': True},
        }

    # 对数据进行额外的校验
    # def validate(self, attrs):
    #     pass

    # 自定定制create，因为保存的数据不仅仅是用提交过来的数据，并且该方法的返回值是新创建的记录的模型类对象
    def create(self, validated_data):

        # 1. self 在这里代表的就是序列化器
        # 2. self.context 是一个字典类型的数据，里面有3个成员，分别是本次客户端的request请求对象，本次调用序列化器的view视图对象，和本次客户端提交请求时的format数据格式
        # 3. self.context 是 ModelSerializerd的父类Serializer->BaseSerializer->Field中定义的，在BaseSerializer中被赋值，本质上就是 BaseSerializer的 _context属性
        # 4. self.context 的最终结果是在通用视图类 ModelViewSet的父类GenericViewSet-->GenericAPIView-->get_serializer_context方法中被最终赋值。
        user_id = self.context['request'].user.id  # 用户信息
        # user_id = 1
        print("validated_data",validated_data)

        new_obj = ReleaseApply.objects.create(**{
            "git_release_branch_or_tag": validated_data.get('git_release_branch_or_tag'),
            "git_release_version": validated_data.get('git_release_version'),
            "name": validated_data.get('name'),
            "git_release_commit_id": validated_data.get('git_release_commit_id'),
            "description": validated_data.get('description'),
            "release_record": validated_data.get('release_record'),
            "user_id": user_id,
        })

        return new_obj

    def update(self, instance, validated_data):
        print(f"instance={instance}, validated_data={validated_data}")
        return super().update(instance, validated_data)
