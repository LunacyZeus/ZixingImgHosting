from django.db import models
from django.utils import timezone

from apps.walrus.managers import PicManager


# Create your models here.

class PicTest(models.Model):
    pic = models.ImageField(upload_to='walrus/')
    created = models.DateTimeField(verbose_name="创建时间", default=timezone.now, blank=True, null=True)

    # 自定义管理器
    objects: PicManager = PicManager()

    class Meta:
        verbose_name = "图片测试"
        verbose_name_plural = "图片测试"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.pic}"


class WalrusFile(models.Model):
    key = models.CharField(max_length=64, unique=True)  # 存储 S3 返回的 key
    content_type = models.CharField(max_length=100, blank=True)  # 文件类型
    size = models.PositiveBigIntegerField(default=0, blank=True)
    remark = models.CharField(verbose_name='备注', max_length=128, default='', blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, auto_created=True)  # 上传时间

    # 自定义管理器
    objects: PicManager = PicManager()

    class Meta:
        verbose_name = "Walrus文件"
        verbose_name_plural = "Walrus文件"
        ordering = ["-created"]
