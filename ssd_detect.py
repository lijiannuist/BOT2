# Detection with SSD
#In this example, we will load a SSD model and use it to detect objects

#1. Setup
#First, Load necessary libs and set up caffe and caffe_root

import numpy as np
import matplotlib.pyplot as plt

'''
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'
'''   
# Make sure that caffe is on the python path:\n"
caffe_root = "/root/caffe"  # this file is expected to be in {caffe_root}/examples
import os
os.chdir(caffe_root)
import sys
sys.path.insert(0, 'python')
import caffe
caffe.set_device(9)
caffe.set_mode_gpu()

from google.protobuf import text_format
from caffe.proto import caffe_pb2
#load PASCAL VOC label
root_dir = "/data2/lijian/BOT2/"
labelmap_file = root_dir + '/code/labelmap_voc.prototxt'
file = open(labelmap_file, 'r')
labelmap = caffe_pb2.LabelMap()
text_format.Merge(str(file.read()), labelmap)

def writetofile(cur_txt_name , product_count , cur_categories , cur_bboxes):    
    with open(cur_txt_name , 'w') as fwrite :
      fwrite.write(str(product_count) + '\n')
      #print cur_categories
      for i in xrange(product_count):
          per_line = cur_categories[i] + ' ' + str(cur_bboxes[i][0]) + ' ' + str(cur_bboxes[i][1]) + ' ' + str(cur_bboxes[i][2]) + ' ' + str(cur_bboxes[i][3]) + '\n'
          #print per_line
          fwrite.write(per_line)       

def get_labelname(labelmap, labels):
        num_labels = len(labelmap.item)
        labelnames = []
        if type(labels) is not list:
            labels = [labels]
        for label in labels:
            found = False
            for i in xrange(0, num_labels):
                if label == labelmap.item[i].label:
                    found = True
                    labelnames.append(labelmap.item[i].display_name)
                    break
            assert found == True
        return labelnames
#Load the net in the test phase for inference, and configure input preprocessing
model_def =root_dir + '/code/deploy.prototxt'
model_weights = root_dir + '/code/VGG_VOC0712_SSD_500x500_iter_100000.caffemodel'
net = caffe.Net(model_def,      # defines the structure of the model\n",
                    model_weights,  # contains the trained weights\n",
                    caffe.TEST)     # use test mode (e.g., don't perform dropout)\n",
# input preprocessing: 'data' is the name of the input blob == net.inputs[0]\n",
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.array([104,117,123])) # mean pixel\n",
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]\n",
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB"

# load a image
image_resize = 500
net.blobs['data'].reshape(1,3,image_resize,image_resize)
im_file = "/data2/lijian/BOT2/testimg1/"
label_file = "/data2/lijian/BOT2/result1/"

for im_name in os.listdir(im_file):
	image = caffe.io.load_image(im_file + im_name)
	print im_name
	# Run the net and examine the top_k results
	transformed_image = transformer.preprocess('data', image)
	net.blobs['data'].data[...] = transformed_image
	# Forward pass
	detections = net.forward()['detection_out']
	# Parse the outputs
	det_label = detections[0,0,:,1]
	det_conf = detections[0,0,:,2]
	det_xmin = detections[0,0,:,3]
	det_ymin = detections[0,0,:,4]
	det_xmax = detections[0,0,:,5]
	det_ymax = detections[0,0,:,6]
		
	# Get detections with confidence higher than 0.6.
	top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.6]
	top_conf = det_conf[top_indices]
	top_label_indices = det_label[top_indices].tolist()
	top_labels = get_labelname(labelmap, top_label_indices)
	top_xmin = det_xmin[top_indices]
	top_ymin = det_ymin[top_indices]
	top_xmax = det_xmax[top_indices]
	top_ymax = det_ymax[top_indices]
	#print top_conf , top_labels
	#print top_xmax , top_ymax
	cur_bboxes = []
	cur_categories = []
	product_count = 0
	for i in xrange(top_conf.shape[0]):
		    xmin = int(round(top_xmin[i] * image.shape[1]))
		    ymin = int(round(top_ymin[i] * image.shape[0]))
		    xmax = int(round(top_xmax[i] * image.shape[1]))
		    ymax = int(round(top_ymax[i] * image.shape[0]))
		    score = top_conf[i]
		    label = int(top_label_indices[i])
		    label_name = top_labels[i]
		    #display_txt = '%s: %.2f'%(label_name, score)
		    #coords = (xmin, ymin), xmax-xmin+1, ymax-ymin+1
		    bbox_cut = [xmin, ymin, xmax, ymax]
		    cur_bboxes.append(bbox_cut)
		    cur_categories.append(label_name)
		    product_count = product_count + 1
			#print display_txt, coords
	cur_txt_name = label_file + im_name.split(".")[0] + ".txt"
	writetofile(cur_txt_name , product_count , cur_categories , cur_bboxes)
		   # color = colors[label]\n",
		   # currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))\n",
		   # currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor':color, 'alpha':0.5})"