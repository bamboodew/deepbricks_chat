from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("欢迎来到数据录入系统！")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),  # 你的API应用
    path("", home),  # 根路径指向 home 视图
]
