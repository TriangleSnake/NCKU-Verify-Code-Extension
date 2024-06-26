from gevent import pywsgi
from flask import Flask, request,make_response,jsonify
from flask_cors import CORS
import base64
import numpy as np
import cv2
app = Flask(__name__)
CORS(app)
def binaziation(image):

    ret, binary = cv2.threshold(image, 30, 255, cv2.THRESH_BINARY)
    return binary

def num_cmp(image1,image2):
    sum = 0
    for i in range(len(image1)):
        for j in range(len(image1[0])):
            if image1[i][j] != image2[i][j]:
                sum += 1
    return sum

def decode_image_from_base64(data):
    image_bytes = base64.b64decode(data)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    return cv2.imdecode(image_np, cv2.IMREAD_COLOR)

def split_image(image):
    per_num=[]
    for i in range(4):   
        per_num.append(cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)[0:20,9+i*9:19+i*9])
    return per_num

def img2txt(image):
    image = binaziation(image)
    min_lst = []
    for i in range(10):
        num_img = cv2.imread(f'{i}.png')
        num_img = cv2.cvtColor(num_img,cv2.COLOR_BGR2GRAY)
        num_img = binaziation(num_img)
        min_lst.append(num_cmp(image,num_img))
    min_val = min(min_lst)
    return str(min_lst.index(min_val))


@app.route('/', methods=['POST','HEAD'])
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
    numbers = split_image(image)
    verify_code = ''
    for i in numbers:
        verify_code += img2txt(i)
    response = make_response(verify_code)
    return response

if __name__ == '__main__':
    server = pywsgi.WSGIServer(("0.0.0.0",5001),app)
    server.serve_forever()
