
import base64
import numpy as np
import cv2

def binaziation(image:cv2.typing.MatLike)->cv2.typing.MatLike:

    ret, binary = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
    cv2.imshow('image',binary)
    cv2.waitKey(0)
    return binary

def num_cmp(image1:cv2.typing.MatLike,image2:cv2.typing.MatLike):
    sum = 0
    
    show_img = np.copy(image1)
    for i in range(len(image1)):
        for j in range(len(image1[0])):
            show_img[i][j] = 255
            if image1[i][j] != image2[i][j]:
                sum += 1
                show_img[i][j] = 0
    return sum

def decode_image_from_base64(data:str)->cv2.typing.MatLike:
    image_bytes = base64.b64decode(data)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    return cv2.imdecode(image_np, cv2.IMREAD_COLOR)

def split_image(image:cv2.typing.MatLike)->list[cv2.typing.MatLike]:
    per_num=[]
    tmp_img = np.copy(image)
    i = 0
    while i < len(image[0]) and len(per_num) < 4:
        #cv2.imshow('image',cv2.resize(tmp_img,(600,150)))
        #cv2.waitKey(30)
        if np.sum(image[:,i] == 0) > 2:
            
            for j in range(len(image)):
                #cv2.imshow('image',cv2.resize(tmp_img,(600,150)))
                #cv2.waitKey(30)
                sum_of_black = np.sum(image[j][i:i+8]==0)
                if sum_of_black > 2:
                    
                    per_num.append(image[j-1:j+10,i-1:i+8])
                    i+=8
                    tmp_img = np.copy(image)
                    
                    break
                else:
                    tmp_img[j] = np.full((len(image[0])),0)
        else:
            tmp_img[:,i] = np.full((len(image)),0)
        
        i+=1
    #for i in per_num:
        #cv2.imshow('image',cv2.resize(i,(80,100)))
        #cv2.waitKey(0)
    return per_num

def img2txt(image:cv2.typing.MatLike)->str:
    image = binaziation(image)
    max_lst = []
    max_lst = [cv2.minMaxLoc(cv2.matchTemplate(image,NUM_IMG[i],cv2.TM_CCORR))[1] for i in range(10)]
    max_val = max(max_lst)
    return str(max_lst.index(max_val))

def remove_noise(image:cv2.typing.MatLike)->cv2.typing.MatLike:
    for i in range(1,len(image)-1):
        for j in range(1,len(image[0])-1):
            if image[i][j] == 0:
                if image[i-1][j] == 255 and image[i+1][j] == 255 and image[i][j-1] == 255 and image[i][j+1] == 255:
                    image[i][j] = 255
    return image

NUM_IMG = []

for i in range(10):
    tmp = cv2.imread(f'{i}_m.png')
    tmp = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY)
    NUM_IMG.append(binaziation(tmp))

'''
for i in range(10):
    image = cv2.imread(f'{i}.png',0)
    image = binaziation(image)
    print(image)
    image = image[6:-4,1:-1]
    cv2.imwrite(f'{i}_m.png',image)
'''

image = cv2.imread('imgcode.png',0)[1:-1,1:-1]
image = binaziation(image)
image = remove_noise(image)
image_lst = split_image(image)
for i in image_lst:
    print("\r",img2txt(i),"    ")
