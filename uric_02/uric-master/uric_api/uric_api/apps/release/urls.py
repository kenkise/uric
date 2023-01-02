from django.urls import path,re_path
from . import views

urlpatterns = [
    path('app', views.ReleaseAPIView.as_view()),

    path('new', views.NewReleaseAPIView.as_view()),
    path('apply', views.ReleaseApplyViewSet.as_view({'get': 'list', 'post': 'create'})),

    # 获取发布申请的状态数据 接口路径
    path('apply/status', views.ReleaseApplyStatus.as_view()),

    path('envs/apps', views.EnvsAppsView.as_view()),

    path('git/branch/', views.GitBranchAPIView.as_view()),
# 审核发布记录的接口，这里仅仅涉及到部分字段的修改，所以我们绑定路由的请求方法使用patch，
    # 调用ModelViewSet中partial_update
    re_path('release_ap/(?P<pk>\d+)/', views.ReleaseApplyViewSet.as_view({'patch': 'partial_update', })),
]
