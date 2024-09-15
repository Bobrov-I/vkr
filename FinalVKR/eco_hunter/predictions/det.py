from ultralytics import YOLO
from PIL import Image

def det(image_path):
    file_img = Image.open(image_path)
    model = YOLO('cv_models/det/YoloV8_det.pt') 
    results = model.predict(file_img, conf = 0.3, device ='cpu', agnostic_nms= True)
    results[0].names[0] = 'Возможно опасные'
    results[0].names[1] = 'Не опасные'
    for result in results:
        bboxes = result.boxes.xyxy.cpu().tolist()
        clss = result.boxes.cls.cpu().tolist()
    count_1 = clss.count(1.0)
    count_0 = clss.count(0.0)
    if bboxes != []:
        im_array = results[0].plot(masks=False)
        img_with_boxes = Image.fromarray(im_array[..., ::-1], 'RGB')
        return img_with_boxes, count_0, count_1
    else: return None, None, None

