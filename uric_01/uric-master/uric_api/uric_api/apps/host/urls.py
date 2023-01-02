from django.urls import path, re_path
from . import views

urlpatterns = [
    path('category/', views.HostCategoryListAPIView.as_view()),  #主机分类数据
    path('host/', views.HostModelViewSet.as_view({'get': 'list', 'post': 'create'})), #主机数据
    path("host_excel", views.HostExcelView.as_view()),
]