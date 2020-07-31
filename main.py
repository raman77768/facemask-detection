import cv2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
import numpy as np
from tensorflow.keras.models import load_model
from keras.preprocessing import image
from skimage.transform import resize
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import os
import subprocess
import ffmpeg
model = load_model("mask_detector.model")
net = cv2.dnn.readNet("deploy.prototxt","res10_300x300_ssd_iter_140000.caffemodel")
print("LIBRARY LOADED")
#VIDEO FUNCTION
def videopred(filename):
  image = cv2.imread('img/'+filename)
  orig = image.copy()
  (h, w) = image.shape[:2]
  blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),(104.0, 177.0, 123.0))
  net.setInput(blob)
  detections = net.forward()
  for i in range(0, detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.5:
      box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
      (startX, startY, endX, endY) = box.astype("int")
      (startX, startY) = (max(0, startX), max(0, startY))
      (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
      face = image[startY:endY, startX:endX]
      face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
      face = cv2.resize(face, (224, 224))
      face = img_to_array(face)
      face = preprocess_input(face)
      face = np.expand_dims(face, axis=0)
      (mask, withoutMask) = model.predict(face)[0]
      label = "Mask" if mask > withoutMask else "No Mask"
      color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
      cv2.putText(image, label, (startX, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
      cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
  cv2.imwrite('outputimg/'+filename,image)

def output_video(filename):
  print("FFMPEG STARTING")
  #filename="C:/Users/Raman/Desktop/mask/"+filename
  subprocess.call("mkdir img",shell=True)
  subprocess.call("mkdir outputimg",shell=True)
  print("folder completed")
  os.system("ffmpeg -i {} -vf fps=1 img/output%06d.jpg".format(filename))
  print("unpacked")
  lst=[]
  lst=os.listdir('img')
  lst.sort()
  for i in lst:
    if '.jpg' in i:videopred(i)

  os.system("ffmpeg -r 1 -f image2 -s 1920x1080 -i outputimg/output%06d.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4 -loglevel quiet")
  print("VIDEO SAVED")
def delete_folder():
  os.system("del img")
  os.system("del outputimg")