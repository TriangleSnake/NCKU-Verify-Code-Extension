function getImageBase64(imgElement, callback) {
    const canvas = document.createElement('canvas');
    canvas.width = imgElement.width;
    canvas.height = imgElement.height;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(imgElement, 0, 0, canvas.width, canvas.height);

    const dataURL = canvas.toDataURL('image/png');
    console.log(dataURL);
    callback(dataURL);
}

function sendCaptchaToServer(base64Image) {
    const url = 'www.trianglesnake.com'
    const apiURL = 'https://'+ url +'/api/captcha';
    fetch(apiURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            image: base64Image,
        }),
    })
    .then(response => response.text())
    .then(text => {        
        console.log('Success:', text);
        document.getElementById('code').value = text;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

const vcode = document.querySelector('img.click');
getImageBase64(vcode, sendCaptchaToServer);
