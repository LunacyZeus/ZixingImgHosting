from django.contrib import admin

from application.admin import admin_site
from apps.walrus import models


# Register your models here.

class PicTestAdmin(admin.ModelAdmin):
    list_display = (
        "pic",
        "created",
    )
    # search_fields = ("container_name", "container_code")
    list_filter = (
        "created",
    )
    actions = []


class WalrusFileAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "content_type",
        "created",
    )
    # search_fields = ("container_name", "container_code")
    list_filter = (
        "created",
    )
    actions = []


admin_site.register(models.PicTest, PicTestAdmin)
admin_site.register(models.WalrusFile, WalrusFileAdmin)
