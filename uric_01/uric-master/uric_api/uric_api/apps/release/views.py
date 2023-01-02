from rest_framework.generics import ListAPIView,CreateAPIView
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