# import base64
# import socketio

# sio = socketio.Client()

# def push(str):
#     with open(str, 'rb') as f:
#         image_data = f.read()
#         image_base64 = base64.b64encode(image_data).decode()
#         sio.connect('http://localhost:3000')
#         sio.emit('imageSent', {'filename': str, 'buffer': image_base64})
#         sio.disconnect()

import socket
import json
def push(strr,namee):
    # set up the file paths for the image and metadata files
    image_file_path = strr

    # open the image file and read its binary data
    with open(image_file_path, 'rb') as image_file:
        image_data = image_file.read()

    # create the JSON payload containing the image data and metadata
    payload = {
        'filename': namee,
        'image_data': image_data.decode('latin1') # convert binary data to string for JSON encoding
    }

    # convert the payload to a JSON string and encode it as bytes
    json_payload = json.dumps(payload).encode('utf-8')

    # create a socket object and connect to the remote server
    server_address = ('http://localhost', 3000) # replace with the actual server address and port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.connect(server_address)

    # send the JSON payload to the server
    sock.sendall(json_payload)

    # receive the server's response (optional)
    response = sock.recv(1024)

    # close the socket connection
    sock.close()
