import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
def writetofile(cur_txt_name , product_count , cur_categories , cur_bboxes):    
    with open(cur_txt_name , 'w') as fwrite :
      fwrite.write(str(product_count) + '\n')
      #print cur_categories
      for i in xrange(product_count):
          per_line = cur_categories[i] + ' ' + str(cur_bboxes[i][0]) + ' ' + str(cur_bboxes[i][1]) + ' ' + str(cur_bboxes[i][2]) + ' ' + str(cur_bboxes[i][3]) + '\n'
          #print per_line
          fwrite.write(per_line)   
   
labelpath = "/data2/lijian/BOT2/38_text/"
imgpath = "/data2/lijian/BOT2/testimg1/"
for idname in os.listdir(labelpath):
   if '_' in idname :
      continue 
   bbox_file = labelpath + idname
   id = idname.split('.')[0]
   print "    " , id
   #-- read img
   #imname = idname.replace('.txt' , '.jpg')
   im = cv2.imread(imgpath + id + ".jpg")
   #print im.shape
   [w,h,c] = im.shape
   #-- read bounding box
   f = open(bbox_file , "r")
   bbox = []
   for line in f.readlines():
      bbox.append( line ) 
   #print bbox
#------------------------------------------------------------------------   
   #-- cut and save img
   im_cut= im[0:int(0.7*w),:,:]
   [w_cut,h_cut,c_cut] = im_cut.shape
   #print im_cut.shape
   cv2.imwrite(imgpath + id + "_up.jpg" , im_cut)
   
   #-- cut and save bbox
   cur_bboxes = []
   cur_categories = []
   product_count = 0
   for i in range(1,int(bbox[0])+1):
          temp = bbox[i].strip("\n").split(" ")
          print temp
          cls=temp[0]
          xmin=int(temp[1])
          ymin=int(temp[2])
          xmax=int(temp[3])
          ymax=int(temp[4])
		  # remove cut bbox 
          #print ymin + (ymax - ymin) * 0.8 ,"---", w_cut
          if (ymax - ymin) * 0.7 < ymax - w_cut : 
              #print ymin + (ymax - ymin) * 0.8 , w_cut
              continue 
          ymax = min(ymax , w_cut)
          bbox_cut = [xmin, ymin, xmax, ymax]
          cur_bboxes.append(bbox_cut)
          cur_categories.append(cls)
          product_count +=1
   print  cur_categories
   cur_txt_name = labelpath + id + "_up.txt"
   writetofile(cur_txt_name , product_count , cur_categories , cur_bboxes)
#------------------------------------------------------------------------   
   #-- cut and save img
   im_cut= im[:,0:int(0.7*h),:]
   [w_cut,h_cut,c_cut] = im_cut.shape
   #print im_cut.shape
   cv2.imwrite(imgpath + id + "_left.jpg" , im_cut)
   
   #-- cut and save bbox
   cur_bboxes = []
   cur_categories = []
   product_count = 0
   for i in range(1,int(bbox[0])+1):
          temp = bbox[i].strip("\n").split(" ")
          print temp
          cls=temp[0]
          xmin=int(temp[1])
          ymin=int(temp[2])
          xmax=int(temp[3])
          ymax=int(temp[4])
		  # remove cut bbox 
          print (xmax - xmin) * 0.3 , xmax , h_cut , int(0.7*h)
          if (xmax - xmin) * 0.7 < xmax - h_cut  : 
              #print ymin + (ymax - ymin) * 0.8 , w_cut
              continue 
          xmax = min(xmax, h_cut)
          bbox_cut = [xmin, ymin, xmax, ymax]
          cur_bboxes.append(bbox_cut)
          cur_categories.append(cls)
          product_count +=1
   print  cur_categories
   cur_txt_name = labelpath + id + "_left.txt"
   writetofile(cur_txt_name , product_count , cur_categories , cur_bboxes)
#------------------------------------------------------------------------   
   #-- cut and save img
   im_cut= im[int(0.3*w):w,:,:]
   [w_cut,h_cut,c_cut] = im_cut.shape
   #print im_cut.shape
   cv2.imwrite(imgpath + id + "_down.jpg" , im_cut)
   
   #-- cut and save bbox
   cur_bboxes = []
   cur_categories = []
   product_count = 0
   for i in range(1,int(bbox[0])+1):
          temp = bbox[i].strip("\n").split(" ")
          print temp
          cls=temp[0]
          xmin=int(temp[1]) 
          ymin=int(temp[2]) 
          xmax=int(temp[3])
          ymax=int(temp[4]) 
		  # remove cut bbox 
          #print ymin + (ymax - ymin) * 0.8 ,"---", w_cut
          if (ymax - ymin) * 0.3 < int(0.3*w) - ymin : 
              #print ymin + (ymax - ymin) * 0.8 , w_cut
              continue 
          ymin -= int(0.3*w)
          ymax -= int(0.3*w)
          ymin = max (1 , ymin)
          bbox_cut = [xmin, ymin, xmax, ymax]
          cur_bboxes.append(bbox_cut)
          cur_categories.append(cls)
          product_count +=1
   print  cur_categories
   cur_txt_name = labelpath + id + "_down.txt"
   writetofile(cur_txt_name , product_count , cur_categories , cur_bboxes)
#------------------------------------------------------------------------   
   #-- cut and save img
   im_cut= im[:,int(0.3*h):h,:]
   [w_cut,h_cut,c_cut] = im_cut.shape
   print h - h_cut , (0.3*h) 
   cv2.imwrite(imgpath + id + "_right.jpg" , im_cut)
   
   #-- cut and save bbox
   cur_bboxes = []
   cur_categories = []
   product_count = 0
   for i in range(1,int(bbox[0])+1):
          temp = bbox[i].strip("\n").split(" ")
          print temp
          cls=temp[0]
          xmin=int(temp[1]) 
          ymin=int(temp[2]) 
          xmax=int(temp[3])
          ymax=int(temp[4]) 
		  # remove cut bbox 
          #print (xmax - xmin) * 0.7 ," ", int(0.3 * h) - xmin
          if (xmax - xmin) * 0.7 < int(0.3*h) - xmin : 
              #print ymin + (ymax - ymin) * 0.8 , w_cut
              continue 
          #print xmin , xmin - int(0.3*h)
          xmin -= int(0.3*h)
          xmax -= int(0.3*h)
          xmin = max (1 , xmin)
          bbox_cut = [xmin, ymin, xmax, ymax]
          cur_bboxes.append(bbox_cut)
          cur_categories.append(cls)
          product_count +=1
   print  cur_categories
   cur_txt_name = labelpath + id + "_right.txt"
   writetofile(cur_txt_name , product_count , cur_categories , cur_bboxes)
   
   
   
