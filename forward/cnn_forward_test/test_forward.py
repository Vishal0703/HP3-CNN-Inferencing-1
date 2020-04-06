import torchvision.models as models
import torch
import torch.nn as nn
import numpy as np
import cv2
import sys

#Load the Image
def loadImage(imagePath):
    img = cv2.imread(imagePath,cv2.IMREAD_COLOR).astype(np.float32)
    res = cv2.resize(img, (255,255))
    res = cv2.normalize(res, res, 0.0, 1.0, cv2.NORM_MINMAX)
    return res


cpp_output = None
with open("final_out.txt", "r") as f:
    lines = f.readlines()
    cpp_output = lines[0].rstrip()
    cpp_output = cpp_output.split(' ')
    cpp_output = [float(x) for x in cpp_output]  

cpp_output = np.asarray(cpp_output)

model = models.vgg19(pretrained=True)
# model = nn.Sequential(*list(vgg19.children())[:2])
print(model)

#Load the image
res = loadImage('forward/data/n02118333_27_fox.jpg')

#Process the image for feeding it to the model appropriately
res = np.reshape(res, (1,res.shape[0],res.shape[1],res.shape[2]))
res = np.transpose(res, (0, 3, 1, 2))

#Create the input tensor
input_tensor = torch.from_numpy(res)

model.eval()
with torch.no_grad():
    output_tensor = model(input_tensor)
    output = output_tensor.numpy()

output = np.reshape(output, (-1,))
print(output.shape)
print(cpp_output.shape)

diff = cpp_output - output
diff = np.abs(diff)
print (np.max(diff))