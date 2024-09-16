"""peer_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path

from application import settings
from application.admin import admin_site
from apps.api import ninja_api
from apps.walrus.views import index_view, show_upload, upload_handle, upload_walrus_handle, list_files

urlpatterns = [
    path("", index_view),
    path("api/", ninja_api.urls),
    path("d_admin/", admin_site.urls),

    path('show_upload/', show_upload),  # 图片上传页
    path('upload_handle/', upload_handle),  # 图片上传处理页
    path('upload_walrus_handle/', upload_walrus_handle),  # 图片上传处理页
    path('img/list/', list_files),  # 返回全部图片接口
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      re_path('^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
