import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import random

def writetofile(cur_txt_name , product_count , cur_categories , cur_bboxes):    
    with open(cur_txt_name , 'w') as fwrite :
      fwrite.write(str(product_count) + '\n')
      #print cur_categories
      for i in xrange(product_count):
          per_line = cur_categories[i] + ' ' + str(cur_bboxes[i][0]) + ' ' + str(cur_bboxes[i][1]) + ' ' + str(cur_bboxes[i][2]) + ' ' + str(cur_bboxes[i][3]) + '\n'
          #print per_line
          fwrite.write(per_line)   

labelpath = "/data2/lijian/BOT2/new_test_labels/"
imgpath = "/data2/lijian/BOT2/testimg1/"

upid = []
downid = []
leftid = []
rightid = []
for idname in os.listdir(labelpath):
  if '_' not in idname :
    continue 
  cls = idname.strip().split('_')[1].split('.')[0]	
  if cls == "up" :
    upid.append(idname)
  if cls == "down" :
    downid.append(idname)
  if cls == "left" :
    leftid.append(idname)
  if cls == "right" :
    rightid.append(idname)

for irand in xrange(1000):
	upindex = random.randrange(0,len(upid))
	downindex = random.randrange(0,len(downid))
	leftindex = random.randrange(0,len(leftid))
	rightindex = random.randrange(0,len(rightid))

	print upid[upindex] , downid[downindex] , leftid[leftindex] , rightid[rightindex]

	upimgid = upid[upindex].split(".")[0]
	downimgid = downid[downindex].split(".")[0]
	upimg = cv2.imread(imgpath + upimgid + ".jpg")
	downimg = cv2.imread(imgpath + downimgid + ".jpg")
	[uph, upw, upc] = upimg.shape
	[downh, downw, downc] =downimg.shape

	#---------------------img
	print upimg.shape , downimg.shape
	maxw = max(upw, downw)
	upimg_resize = cv2.resize(upimg , (maxw, uph), interpolation = cv2.INTER_CUBIC)
	downimg_resize = cv2.resize(downimg , (maxw , downh), interpolation = cv2.INTER_CUBIC)
	newimg = np.zeros((uph+downh,maxw, upc),dtype=upimg.dtype)
	print newimg.shape , upimg_resize.shape , downimg_resize.shape
	newimg[0:uph,:,:] = upimg_resize
	newimg[uph:uph+downh,:,:] = downimg_resize
	cv2.imwrite(imgpath + upimgid + downimgid + ".jpg" , newimg)

	#---------------------label
	cur_bboxes = []
	cur_categories = []
	product_count = 0
	upf = open(labelpath + upid[upindex] , "r")
	upbbox = []
	for line in upf.readlines(): 
			  upbbox.append( line ) 
	for i in range(1,int(upbbox[0])+1):
	  temp = upbbox[i].strip("\n").split(" ")
	  print temp
	  cls=temp[0]
	  xmin=int(float(temp[1])/upw*maxw)
	  ymin=int(temp[2])
	  xmax=int(float(temp[3])/upw*maxw)
	  ymax=int(temp[4])
	  bbox_cut = [xmin, ymin, xmax, ymax]
	  cur_bboxes.append(bbox_cut)
	  cur_categories.append(cls)
	  
	downf = open(labelpath + downid[downindex] , "r")
	downbbox = []
	for line in downf.readlines(): 
			  downbbox.append( line ) 
	for i in range(1,int(downbbox[0])+1):
	  temp = downbbox[i].strip("\n").split(" ")
	  print temp
	  cls=temp[0]
	  xmin=int(float(temp[1])/downw*maxw)
	  ymin=int(temp[2]) + uph
	  xmax=int(float(temp[3])/downw*maxw)
	  ymax=int(temp[4]) + uph
	  bbox_cut = [xmin, ymin, xmax, ymax]
	  cur_bboxes.append(bbox_cut)
	  cur_categories.append(cls)

	product_count = int(downbbox[0]) + int(upbbox[0])
	cur_txt_name = labelpath +upimgid + downimgid + ".txt"
	print upimgid + downimgid 
	writetofile(cur_txt_name , product_count , cur_categories , cur_bboxes)
  #print len(upid) + len(downid) + len(leftid) +  len(rightid)













