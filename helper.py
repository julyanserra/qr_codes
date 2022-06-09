import hashlib, binascii, os
import qrcode
from cloudinary.uploader import upload
from PIL import Image
import io
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, g, redirect, Response, session, flash
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload


base_url = "https://qr-shirts-daddy.herokuapp.com"
shirt_host = os.getenv("SHIRT_HOST", base_url+"/shirt/")
temp_location = '/tmp/'
UPLOAD_FOLDER = temp_location + 'images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
env = os.getenv("ENV", "dev")

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def image_to_byte_array(image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

def generateQR(link):
    qr = qrcode.QRCode(version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )

    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image()
    return img

def getQrId(shirt_id):
    #### generate qr code
    link = shirt_host + str(shirt_id)
    qr = image_to_byte_array(generateQR(link))
    temp_file = temp_location+'qr'+str(shirt_id)+'.jpg'
    image_file = open(temp_file, 'wb')
    image_file.write(qr)
    image_file.close()
    #lets fetch the shirt
    response = upload(temp_file)
    qr_id = response['public_id']
    return qr_id

def handleImageUpload(request):
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return None
    if file and allowed_file(file.filename):
        response = upload(file)
        return response['public_id']

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getImageUrl(id):
    if(env == 'prod'):
        return cloudinary_url(id)
    else:
        return "static/assets/images/stm_logo.png", ""
