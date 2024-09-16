import jmespath
from django.http import HttpResponse
from django.shortcuts import render

from application.settings import MEDIA_ROOT
from apps.walrus.models import PicTest
from pkg.response.response import APIResponse
from pkg.utils.http.walrus.web import send_file_to_remote_server

# 定义文件大小限制，10MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


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


def upload_walrus_handle(request):
    pic = request.FILES['pic']

    if pic:

        # 检查文件大小是否超过10MB
        if pic.size > MAX_FILE_SIZE:
            # return JsonResponse({'status': 'failed', 'error': 'File size exceeds 10MB limit'}, status=400)
            return APIResponse(code=403, msg='File size exceeds 10MB limit')

        resp_json = send_file_to_remote_server(pic)
        print(resp_json)
        # {'alreadyCertified': {'blobId': '3XclPOZhFmt0JarSQrWO8kc8Nm_5ewUHbLBdM5VrUWw', 'event': {'txDigest': 'DHtz5Sb4xUoyeYWmmnY76xV1c26EcxNHPRGKeqTF7H2r', 'eventSeq': '0'}, 'endEpoch': 5}}
        '''
        {'newlyCreated': {'blobObject': {'id': '0x4a3d2c7eab6ad0498b7b8d4aac287bb02073779ae4599b36e49b2656493d83ba', 'storedEpoch': 0, 'blobId': '8igW-1ivpxEazhuMm7V9Brg_5I8ykVgV1eaXaj6HQgI', 
'size': 1082394, 'erasureCodeType': 'RedStuff', 'certifiedEpoch': 0, 'storage': {'id': '0x9b15940e5232476299e43d03432513183fc819d5c19bfabc1e4eb93e7658f4eb', 'startEpoch': 0, 'endEpoch'
: 5, 'storageSize': 68987000}}, 'encodedSize': 68987000, 'cost': 16842750}}
        '''
        if 'alreadyCertified' in resp_json:  # 图片已存在
            blob_id = jmespath.search("alreadyCertified.blobId", resp_json)
            # return HttpResponse(f'上传成功，图片id：{blob_id}')
            return APIResponse(code=0, msg='', data={'blob_id': blob_id})
        elif 'newlyCreated' in resp_json:
            blob_id = jmespath.search("newlyCreated.blobObject.blobId", resp_json)
            return APIResponse(code=0, msg='', data={'blob_id': blob_id})

        return APIResponse(code=500, msg='failed resp,please contact author')

    return APIResponse(code=500, msg='plsease provide img file')
