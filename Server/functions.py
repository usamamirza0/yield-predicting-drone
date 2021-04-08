import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import torch
import requests

def initialize():
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    torch.cuda.empty_cache()
    print(device)

    print("Loading Model...")
    model = torch.load("model.pt", map_location=torch.device(device))
    model.to(device)
    model.eval()
    print("Model Loaded")
    return model, device

def read_image(filename, device):
    print("Loading Image...")
    image1 = plt.imread(filename) / 255
    images = [torch.tensor(image1).permute(2,0,1).to(device).to(torch.float32)]
    print("Image Loaded")
    return images

def run_model(model, image):
    print("Running Model...")
    prediction = model(image)
    print("Model run")
    return prediction

def save_image(images, prediction):
    print("Saving Image...")
    fig, ax = plt.subplots(figsize = (10,10))
    img = images[0].permute(1,2,0).cpu().numpy()
    thresh = 0.5
    box_preds = prediction[0]['boxes'].cpu().detach().numpy()
    score_preds = prediction[0]['scores'].cpu().detach().numpy()
    box_preds = box_preds[score_preds >= thresh].astype(np.int32)
    for box in box_preds:
        rect = patches.Rectangle((box[0],box[1]),box[2] - box[0],box[3] - box[1],linewidth=2,edgecolor='r',facecolor='none')
        ax.add_patch(rect)
    ax.set_axis_off()
    ax.imshow(img)
    fig.savefig("static\\result.jpg", bbox_inches='tight', pad_inches=0)
    print("Image Saved")
    return box_preds
    
def get_yield(box_preds):
    # 30 spikelets per head
    # 2.5 grains per spikelets
    # mass of grain = 0.065g
    # 1 hectare = 10000m^2
    # 30 * 2.5 * 0.065 * 0.001 * 10000 = 48.75
    return (len(box_preds) * 48.75)

def my_yield(filename, model, device):
    image = read_image(filename, device)
    prediction = run_model(model, image)
    box_preds = save_image(image, prediction)
    yield_estimate = get_yield(box_preds)
    return yield_estimate

def request_data():
    r = requests.post(url)
    status = r.headers['my-custom-header']
    print(status)