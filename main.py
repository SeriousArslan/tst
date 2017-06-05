import socket
import struct
import cv2
import numpy as np

from cStringIO import StringIO

def create_opencv_image_from_stringio(img_stream, cv2_img_flag=0):
    img_stream.seek(0)
    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    return cv2.imdecode(img_array, cv2_img_flag)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 80))
s.listen(1000)

client, addr = s.accept()
print 'got connected from', addr

buf = ''
while len(buf)<4:
    buf += client.recv(4-len(buf))
size = struct.unpack('!i', buf)
print "receiving %s bytes" % size

with open('tst.jpg', 'wb+') as img:
    while True:
        data = client.recv(1024)
        if not data:
            break
        img.write(data)
    print 'received, yay! img type:', type(img)
    res = create_opencv_image_from_stringio(img)
    # cv2.imshow("im", res)
    # cv2.waitKey(0)

client.close()