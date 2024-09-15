from .models import Requestion, Task, RequisitionImg, Organisation
from django.shortcuts import render
import folium
import io
from django.core.files.base import ContentFile
from .predictions.seg import seg
from .predictions.det import det
from django.db.models import Q
import datetime

def home(request):
    returnequisitions = Requestion.objects.all()
    tasks = Task.objects.filter(holding_date__gte=datetime.date.today())
    organisations = Organisation.objects.all()
    m = folium.Map(location=[64.5401, 40.5433], zoom_start=11, attributionControl=0)
    if returnequisitions != 0:
        len_req = len(returnequisitions)
        for returnequisition in returnequisitions:
            coordinates = (returnequisition.latitude, returnequisition.longitude)
            popup_content = f"""
                <img src="{returnequisition.img.url}" width="150px">
                <p>{returnequisition.address}<br>
                Дата: {returnequisition.date_time.strftime('%d.%m.%Y')}</p>
            """
            popup = folium.Popup(popup_content, max_width=300)
            folium.Marker(coordinates, popup=popup).add_to(m)
    else: pass
    len_tasks = len(tasks)
    len_orgs = len(organisations) 
    context = {
        'map': m._repr_html_(), 
        'len_req':len_req, 
        'len_tasks':len_tasks, 
        'len_orgs':len_orgs, 
        'tasks':tasks, 
        'orgs': organisations}
    return render(request, 'eco_hunter/home.html', context=context)
def fraction_counter(img_dict):
    dan_counter = 0
    nondan_counter = 0
    for img in img_dict:
        if img.predicted_danger_item is not None:
            dan_counter += img.predicted_danger_item
        if img.predicted_nondanger_item is not None:
            nondan_counter += img.predicted_nondanger_item
    if dan_counter != 0 and nondan_counter != 0:
        return f"Обнаружено {dan_counter} возможно опасной фракции", f"Обнаружено {nondan_counter} не опасной фракции"
    elif dan_counter != 0:
        return f"Обнаружено {dan_counter} возможно опасной фракции", None
    elif nondan_counter != 0:
        return None, f"Обнаружено {nondan_counter} не опасной фракции"
    else:
        return None, None
def clss_counter(img_dict):
    clss_count = []
    for img in img_dict:
        if img.cls_predict is not None:
            clss_count.append(img.cls_predict)

    if not clss_count:
        return None     
    if 0 in clss_count:
        return "Опасные отходы"
    else: return "Безопасне отходы"

def requestion(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        files = request.FILES.getlist('photos')
        requisition = Requestion(    
            name=name,
            phone=phone,
            email=email,
            address=address,
            description=description,
            latitude=latitude,
            longitude=longitude,
        )
        requisition.save()
        requisition.img = files[0]
        requisition.save(update_fields=["img"])
        # Обработка загруженных файлов
        files = request.FILES.getlist('photos')
        for file in files:
            name = file.name
            img_byte_arr = io.BytesIO()
            image = RequisitionImg(requisition_img=requisition, image=file)
            image.save()
            # Сегментация файлов
            img_with_boxes, cls_predict = seg(file)
            if img_with_boxes != None:
                img_with_boxes.save(img_byte_arr, format='JPEG') 
                content_file_seg = ContentFile(img_byte_arr.getvalue(), name=name)
                image.img_with_boxes_seg = content_file_seg
                image.cls_predict = cls_predict
                image.save(update_fields=["img_with_boxes_seg", 
                                          "cls_predict"])
            else: # Иначе детекция
                img_with_boxes_det, count_0, count_1 = det(file)
                if img_with_boxes_det != None:
                    img_with_boxes_det.save(img_byte_arr, format='JPEG') 
                    content_file_det = ContentFile(img_byte_arr.getvalue(), name=name)
                    image.img_with_boxes_det = content_file_det
                    image.predicted_danger_item = count_0
                    image.predicted_nondanger_item = count_1
                    image.save(update_fields=["img_with_boxes_det", 
                                              "predicted_danger_item", 
                                              "predicted_nondanger_item"])
        # Получаем сохраненные фото
        predicted_images = RequisitionImg.objects.filter(requisition_img=requisition)
        pred_status = clss_counter(predicted_images)
        requisition.pred_status = pred_status
        requisition.save(update_fields=["pred_status"]) 
        requisition.fraction_status_danger, requisition.fraction_status_nondanger = fraction_counter(predicted_images)
        requisition.save(update_fields=["fraction_status_danger", 
                                        "fraction_status_nondanger"])    
        return render(request, 'eco_hunter/requestion.html')
    return render(request, 'eco_hunter/requestion.html')

def requestions_list(request):
    returnequisitions = Requestion.objects.all()
    valid_returnequisitions = returnequisitions.filter(
    Q(pred_status__isnull=False) | 
    Q(fraction_status_danger__isnull=False) |
    Q(fraction_status_nondanger__isnull=False))
    return render(request, 'eco_hunter/req_archive.html', {'req': valid_returnequisitions})

def requestion_detail(request, pk):
    requestion = Requestion.objects.get(id=pk)
    imgs = RequisitionImg.objects.filter(requisition_img=requestion)
    valid_imgs = imgs.exclude(
    Q(img_with_boxes_seg__exact='') & Q(img_with_boxes_det__exact=''))
    return render(request, 'eco_hunter/req_page.html', {'requestion': requestion, 'imgs': valid_imgs })