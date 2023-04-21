import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

def push(im_name):
    # Initialize Firebase with your credentials
    cred = credentials.Certificate(os.environ("sdk_key"))
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://pixeler-redbus-hackathon-default-rtdb.firebaseio.com/'
    })

    # Reference to the Firebase Realtime Database root
    ref = db.reference('/')

    # converting image to long binary
    with open("temp_image.jpg", 'rb') as image_file:
        image_data = image_file.read()
    

    # Define your JSON object
    data = {
        'name': im_name,
        'image_data': image_data.decode('latin1'),
    }

    # Send the JSON object to Firebase Realtime Database
    ref.set(data)
