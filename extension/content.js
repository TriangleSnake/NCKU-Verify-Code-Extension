function getImageBase64(imgElement, callback,isMoodle) {
    if (!imgElement || !imgElement.src) {
        console.error('No image');
        return;
    }
    const canvas = document.createElement('canvas');
    canvas.width = imgElement.width;
    canvas.height = imgElement.height;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(imgElement, 0, 0, canvas.width, canvas.height);

    const dataURL = canvas.toDataURL('image/png');
    console.log(dataURL);
    callback(dataURL,isMoodle);
}

function sendCaptchaToServer(base64Image,isMoodle) {
    //const apiURL = 'http://localhost:5001/captcha?moodle=' + isMoodle; // for local testing
    const apiURL = 'https://api.trianglesnake.com/captcha?moodle=' + isMoodle; // for production
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
        if(isMoodle)
            document.getElementById('reg_vcode').value = text;
        else
            document.getElementById('code').value = text;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

var vcode = document.querySelector('img.click');
getImageBase64(vcode, sendCaptchaToServer,0);

vcode = document.getElementById('imgcode');
getImageBase64(vcode, sendCaptchaToServer,1);