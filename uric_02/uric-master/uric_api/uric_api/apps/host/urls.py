from django.urls import path,re_path
from . import views

urlpatterns = [
    path("categorys/", views.HostCategoryListAPIView.as_view()),
    path("host_excel", views.HostExcelView.as_view()),
    re_path('^file/(?P<pk>\d+)/$', views.HostFileView.as_view({'get': 'get_folders','post': 'upload_file', 'delete': 'delete_file'})),
]

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("list", views.HostModelViewSet, basename="list"),

urlpatterns +=router.urls