import base64
import socketio

sio = socketio.Client()

def push(str):
    with open(str, 'rb') as f:
        image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode()

        sio.connect('http://localhost:3000')
        sio.emit('image', {'filename': 'image.jpg', 'buffer': image_base64})
        sio.disconnect()
