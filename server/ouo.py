
import base64
import numpy as np
import cv2
import time

def binaziation(image:cv2.typing.MatLike)->cv2.typing.MatLike:

    ret, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    return binary

def num_cmp(image1,image2):
    sum = 0
    for i in range(len(image1)):
        for j in range(len(image1[0])):
            if image1[i][j] != image2[i][j]:
                sum += 1
    return sum

def decode_image_from_base64(data:str)->cv2.typing.MatLike:
    image_bytes = base64.b64decode(data)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    return cv2.imdecode(image_np, cv2.IMREAD_COLOR)

def split_image(image:cv2.typing.MatLike)->list[cv2.typing.MatLike]:
    per_num=[]
    tmp_img = np.copy(image)
    for i in range(len(image[0])):
        cv2.imshow('image',tmp_img)
        cv2.waitKey(0)
        if np.sum(image[:,i] == 0) > 2:
            #image[:,i] = np.full((len(image)),0)
            for j in range(len(image)):
                cv2.imshow('image',tmp_img)
                cv2.waitKey(0)
                print(np.sum(image[j][i:i+8]==0),image[j][i:i+8])
                if  np.sum(image[j][i:i+8]==0)> 2:
                    
                    #image[j] = np.full((len(image[0])),0)
                    per_num.append(tmp_img[j:j+10,i:i+8])
                    break
                else:
                    tmp_img[j] = np.full((len(image[0])),0)
        else:
            tmp_img[:,i] = np.full((len(image)),0)
    return per_num

def img2txt(image:cv2.typing.MatLike)->str:
    image = binaziation(image)
    min_lst = []
    min_lst = [num_cmp(image,NUM_IMG[i]) for i in range(10)]
    min_val = min(min_lst)
    return str(min_lst.index(min_val))

def remove_noise(image:cv2.typing.MatLike)->cv2.typing.MatLike:
    for i in range(1,len(image)-1):
        for j in range(1,len(image[0])-1):
            if image[i][j] == 0:
                if image[i-1][j] == 255 and image[i+1][j] == 255 and image[i][j-1] == 255 and image[i][j+1] == 255:
                    image[i][j] = 255
    return image

NUM_IMG = []

for i in range(10):
    tmp = cv2.imread(f'{i}.png')
    tmp = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY)
    NUM_IMG.append(binaziation(tmp))



image = cv2.imread('imgcode.png',0)[1:-1,1:-1]
cv2.imshow('image',image)
cv2.waitKey(0)
image = binaziation(image)
cv2.imshow('image',image)
cv2.waitKey(0)
image = remove_noise(image)
cv2.imshow('image',image)
cv2.waitKey(0)
image_lst = split_image(image)
for i in image_lst:
    cv2.imshow('image',i)
    cv2.waitKey(0)
