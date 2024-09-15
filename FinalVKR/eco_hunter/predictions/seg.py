from ultralytics import YOLO
from PIL import Image
from eco_hunter.predictions.cls import cls


def seg(image_path):
    file_img = Image.open(image_path)
    model = YOLO('cv_models/seg/YoloV8_seg.pt') 
    results = model.predict(file_img, device ='cpu',retina_masks = True, max_det =1)
    results[0].names[0] = 'Обнаружен мусор'

  
    for result in results:
        bboxes = result.boxes.xyxy.cpu().tolist()
    
    if bboxes != []:
        im_array = results[0].plot(masks=True)
        # Тот самый файл который уже можно сохранять в бд
        img_with_boxes = Image.fromarray(im_array[..., ::-1], 'RGB')        
        #Ограничиваем облассть для cls рамкой сегментатора
        x1, y1, x2, y2 = results[0].boxes[0].xyxy[0]
        crop = results[0].orig_img[int(y1):int(y2), int(x1):int(x2),::-1]
        crop_image = Image.fromarray(crop.astype("uint8"))
        cls_predict = cls(crop_image) #int 0 danger, 1 nondanger
        return img_with_boxes, cls_predict
    else: return None, None













