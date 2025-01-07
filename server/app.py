from gevent import pywsgi
from flask import Flask, request,make_response,jsonify
from flask_cors import CORS
import base64
import numpy as np
import cv2

def binaziation(image:cv2.typing.MatLike,threadshold:int)->cv2.typing.MatLike:
    ret, binary = cv2.threshold(image, threadshold, 255, cv2.THRESH_BINARY)
    return binary


def decode_image_from_base64(data:str)->cv2.typing.MatLike:
    image_bytes = base64.b64decode(data)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    return cv2.imdecode(image_np, cv2.IMREAD_COLOR)

def split_image(image:cv2.typing.MatLike)->list[cv2.typing.MatLike]:
    per_num=[]
    for i in range(4):   
        per_num.append(image[0:20,9+i*9:19+i*9])
    return per_num

def split_image_m(image:cv2.typing.MatLike)->list[cv2.typing.MatLike]:
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
                    
                    per_num.append(image[j:j+10,i:i+8])
                    i+=8
                    tmp_img = np.copy(image)
                    break
                else:
                    tmp_img[j] = np.full((len(image[0])),0)
        else:
            tmp_img[:,i] = np.full((len(image)),0)
        
        i+=1
    return per_num

def img2txt(image:cv2.typing.MatLike)->str:
    
    max_lst = []
    max_lst = [cv2.matchTemplate(image,NUM_IMG[i],cv2.TM_CCOEFF_NORMED) for i in range(10)]
    max_val = max(max_lst)
    return str(max_lst.index(max_val))

def img2txt_m(image:cv2.typing.MatLike)->str:
    
    image = remove_noise(image)
    max_lst = []
    max_lst = [cv2.matchTemplate(image,NUM_IMG_MOODLE[i],cv2.TM_CCOEFF_NORMED) for i in range(10)]
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
    tmp = cv2.imread(f'{i}.png',0)
    NUM_IMG.append(tmp)

NUM_IMG_MOODLE = []
for i in range(10):
    tmp = cv2.imread(f'{i}_m.png',0)
    NUM_IMG_MOODLE.append(tmp)

app = Flask(__name__)
CORS(app)


@app.route('/captcha', methods=['POST','HEAD'])
def api():
    if request.method == 'HEAD':
        response = make_response('ok')
        return response
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'Missing image data'}), 400
    base64_image = data['image']
    if ',' in base64_image:
        base64_image = base64_image.split(',')[1]
    else :
        return jsonify({'error': 'base6 decode error'}), 400
    image = decode_image_from_base64(base64_image)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    verify_code = ''
    if request.args.get("moodle") == '1':
        image = binaziation(image,150)
        image = image[1:-1,1:-1]
        numbers = split_image_m(image)
        for i in numbers:
            verify_code += img2txt_m(i)    

    else:
        image = binaziation(image,30)
        numbers = split_image(image)
        for i in numbers:
            verify_code += img2txt(i)
    print(verify_code)
        
    response = make_response(verify_code)
    return response





if __name__ == '__main__':
    server = pywsgi.WSGIServer(("0.0.0.0",5001),app)
    server.serve_forever()


