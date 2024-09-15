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
