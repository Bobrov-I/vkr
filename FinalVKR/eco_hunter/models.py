from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

def get_upload_path_img(instance, filename):
    return f'images/{instance.id}/garb/{filename}'

def get_upload_path(instance, filename):
    return f'images/{instance.requisition_img.id}/{filename}'

def get_upload_path_boxes(instance, filename):
    return f'images/{instance.requisition_img.id}/boxes/{filename}'

def get_upload_path_logo(instance, filename):
    return f'logos/{instance.organisation_name}/{filename}'

class Requestion(models.Model):
    name = models.CharField(max_length=64, verbose_name="Имя отправителя")
    phone = models.CharField(max_length=64, verbose_name="Телефон")
    email = models.EmailField(max_length=256, verbose_name="Почта")
    address = models.CharField(max_length=512, verbose_name="Адрес свалки")    
    description = models.CharField(max_length=512, default= '-', verbose_name="Описание места свалки") 
    latitude = models.FloatField(max_length=128, default= 1.1, verbose_name="Широта")
    longitude = models.FloatField(max_length=128 , default= 1.1, verbose_name="Долгота")
    date_time = models.DateTimeField(default=timezone.now, verbose_name="Дата обращения")
    pred_status = models.CharField(max_length=32,null=True, default='', verbose_name="Вид отходов")
    fraction_status_danger = models.CharField(max_length=64,null=True, default='', verbose_name="Опасной фракции")
    fraction_status_nondanger = models.CharField(max_length=64,null=True, default='', verbose_name="Безопасной фракции")
    img = models.ImageField(upload_to = get_upload_path_img, verbose_name="Путь к файлу")

    def __str__(self):
        return f'{self.id}. {self.address}'
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

class RequisitionImg(models.Model):
    requisition_img = models.ForeignKey(Requestion,on_delete=models.CASCADE, verbose_name="Адрес")
    image = models.ImageField(upload_to = get_upload_path, verbose_name="Путь к исходному фото")
    img_with_boxes_seg = models.ImageField(upload_to = get_upload_path_boxes, null=True, verbose_name="Путь к сегментированному фото")
    img_with_boxes_det = models.ImageField(upload_to = get_upload_path_boxes, null=True, verbose_name="Путь к фото с детекцией фракций")
    cls_predict = models.IntegerField(null=True, default=None, verbose_name="0-опасная|1-безопасная")
    predicted_danger_item = models.IntegerField(null=True, default=None, verbose_name="Опасной фракции")
    predicted_nondanger_item = models.IntegerField(null=True, default=None, verbose_name="Безопасной фракции")
    def __str__(self):
        return mark_safe(f'<h1>Заявка №{self.requisition_img.id}, фото_ID: {self.id}</h1><p>адрес- {self.requisition_img.address}<p>')
    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии' 
  
class Organisation(models.Model):
    organisation_name = models.CharField(max_length=256, null=True, verbose_name="Название организации")
    logo_organisation = models.ImageField(upload_to = get_upload_path_logo, null=True, verbose_name="Путь к логотипу")
    organisation_link = models.CharField(max_length=256, null=True, verbose_name="Ссылка на страницу|сайт организации")
    phone = models.CharField(max_length=64, verbose_name="Телефон")
    email = models.EmailField(max_length=256, verbose_name="Почта")
    def __str__(self):
        return self.organisation_name
    class Meta:
        verbose_name = 'Организаця'
        verbose_name_plural = 'Организации'
   
class Task(models.Model):
    requisition_task = models.ForeignKey(Requestion, on_delete=models.CASCADE, verbose_name="Адрес")
    organisation = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING, null=True, verbose_name="Организация")
    holding_date = models.DateTimeField(null = True, verbose_name="Дата провеления")
    date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    title = models.CharField(max_length=100,default='', verbose_name="Название мероприятия")
    text = models.TextField(max_length=2000, default='', verbose_name="Описание")
    def __str__(self):
        return mark_safe(f'<h3>{self.holding_date.strftime("%d.%m.%Y в %H:%M")}</h3><p>{self.organisation.organisation_name}<br>{self.requisition_task.address}</p>')
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
    
    
