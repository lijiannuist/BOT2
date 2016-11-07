import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.pyplot import savefig

def plot_detection(im_file,bbox_file):
  im = cv2.imread(im_file)
  im = im[:, :, (2, 1, 0)]
  fig, ax = plt.subplots(figsize=(12, 12))
  ax.imshow(im)
  f = open(bbox_file , "r")
  bbox = []
  bboxnum = 0
  for line in f.readlines():
      bboxnum = bboxnum + 1
      bbox.append( line )
  print type(bbox[0])
  for i in range(1,int(bboxnum)+1):
          temp = bbox[i].strip("\n").split(" ")
          print temp
          cls=temp[0]
          xmin=int(temp[1])
          ymin=int(temp[2])
          xmax=int(temp[3])
          ymax=int(temp[4])
          ax.add_patch(plt.Rectangle((xmin, ymin),xmax - xmin,ymax - ymin, fill=False,edgecolor='red', linewidth=3.5))
          ax.text(xmin , ymin , cls , bbox=dict(facecolor='blue', alpha=0.5) , fontsize=14, color='white')
  plt.axis('off')
  plt.tight_layout()
  plt.draw()
  plt.show()
id ="000000"
im_file = "Z:\\lijian\\plate\\testimages\\" + id + ".jpg"
bbox_file = "Z:\\lijian\\plate\code\result_3W_0.14\\" + id + ".txt"
#bbox_file = "Z:\\lijian\\BOT2\\1000_0.85\\" + id + ".txt"
plot_detection(im_file,bbox_file)
