from django.contrib import admin
from .models import Requestion, Task, RequisitionImg, Organisation
from django.utils.safestring import mark_safe

admin.site.register(Task)

@admin.register(Requestion)
class RequestionAdmin(admin.ModelAdmin):
    list_display = ("address","date_time","get_image")
    readonly_fields = ("get_normal_image",)

    def get_normal_image(self, obj):
        return mark_safe(f'<img src="{obj.img.url}" height="100%"')

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.img.url}" height="150px"')
    
    get_normal_image.short_description =  "Превью свалки"
    get_image.short_description = "Превью свалки"


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("organisation_name","phone","get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.logo_organisation.url}" height="150px"')
    get_image.short_description = "Лого"


@admin.register(RequisitionImg)
class RequisitionImgAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_image")
    readonly_fields = ("get_normal_image",)

    def get_image(self, obj):
        if obj.img_with_boxes_seg and obj.img_with_boxes_seg.url != '':
            return mark_safe(f'<img src="{obj.img_with_boxes_seg.url}" height="200px"')
        elif obj.img_with_boxes_det and obj.img_with_boxes_det.url != '':
            return mark_safe(f'<img src="{obj.img_with_boxes_det.url}" height="200px"')
        else:
            return mark_safe(f'<h1>Мусор не обнаружен</h1>')
    
    def get_normal_image(self, obj):
        if obj.img_with_boxes_seg and obj.img_with_boxes_seg.url != '':
            return mark_safe(f'<img src="{obj.img_with_boxes_seg.url}" height="100%"')
        elif obj.img_with_boxes_det and obj.img_with_boxes_det.url != '':
            return mark_safe(f'<img src="{obj.img_with_boxes_det.url}"height="100%"')
        else:
            return mark_safe(f'<h1>Мусор не обнаружен</h1>')
    get_image.short_description = "Фото мусора"
    get_normal_image.short_description =  "Фото мусора"