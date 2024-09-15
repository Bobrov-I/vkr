import torch
import torch.nn as nn
from torchvision import models, transforms

def cls(img):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = models.densenet121()
    num_ftrs = model.classifier.in_features
    model.classifier = nn.Sequential(
        nn.Dropout(0.5),  
        nn.Linear(num_ftrs, 2) 
    )
    model.load_state_dict(torch.load('cv_models/cls/bestDenseNet121.pth', map_location=device))  
    model = model.to(device)
    model.eval()
    # Предобработка изображения
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image)
        _, preds = torch.max(outputs, 1)
        return preds.item()




