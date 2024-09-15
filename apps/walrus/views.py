from django.http import HttpResponse
from django.shortcuts import render

from application.settings import MEDIA_ROOT
from apps.walrus.models import PicTest
from pkg.response.response import APIResponse


# Create your views here.

def index_view(request):
    return APIResponse(code=0, msg="success")


# /show_upload
def show_upload(request):
    '''图片上传页'''
    return render(request, 'walrus/upload.html')


# /upload_handle
# 图上上传处理,图片2种类型：
# 小于2.5M放在内存中：<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
# 大于2.5放在硬盘上：<class 'django.core.files.uploadedfile.TemporaryUploadedFile'>
def upload_handle(request):
    '''图片上传处理页'''
    # 【1】得到图片
    pic = request.FILES['pic']
    # 【2】拼接图片保存路径+图片名
    save_dir = MEDIA_ROOT / 'walrus'
    if not save_dir.exists():
        return HttpResponse('存储路径不存在')

    save_path = save_dir / pic.name
    if save_path.exists():
        return HttpResponse('图片已存在')

    # 【3】保存图片到指定路径，因为图片是2进制式，因此用wb，
    with open(save_path, 'wb') as f:
        # pic.chunks()为图片的一系列数据，它是一一段段的，所以要用for逐个读取
        for content in pic.chunks():
            f.write(content)

    # 【4】保存图片路径到数据库，此处只保存其相对上传目录的路径
    PicTest.objects.create(pic='static/walrus/%s' % pic.name)

    # 【5】别忘记返回信息
    return HttpResponse('上传成功，图片地址：walrus/%s' % pic.name)
