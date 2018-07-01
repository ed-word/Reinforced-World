
# coding: utf-8

# In[1]:


# Crash Catcher: DashCam Accident Detector  </br>
### Determining whether dashboard camera video contains an accident</br></br>
# I use a hierchical recurrent neural network implementation, trained on a set of videos with and without accidents, to determine whether a new video contains an accident or not.</br></br></br> 


# Load in necessary packages

## we want any plots to show up in the notebook
## has the usual packages I use
import numpy
import os
import re
import pickle
import timeit
import glob
import cv2

from skimage import transform
import skimage
from skimage import io

import sklearn
from sklearn.model_selection import train_test_split   ### import sklearn tool

import keras
from keras.preprocessing import image as image_utils
from keras.callbacks import ModelCheckpoint
import shutil

# In[17]:


# First, write a function to load in a video (.mp4 format, 720 by 1280 in size) from file.
# Each frame of the video will be converted to an image that can be processed.
# 
# In order to make the process (marginally) less memory-intensive, we downscale the image to
# a size of 144 pixels by 256 pixels. In addition, because the images are originally in RGB color,
# we convert to gray-scale. This also reduces the amount of memory, and while some useful information
# may be lost, the color variations from scene to scene (or dashcam to dashcam) are less important.
# Further, losing the color dimension turns a 5-D problem into a 4-D problem -- a bit more tractable.


### here is the function to load in a video from file for analysis

def load_set(videofile):
    '''The input is the path to the video file - the training videos are 99 frames long and have resolution of 720x1248
       This will be used for each video, individially, to turn the video into a sequence/stack of frames as arrays
       The shape returned (img) will be 99 (frames per video), 144 (pixels per column), 256 (pixels per row))
    '''
    ### below, the video is loaded in using VideoCapture function
    images = os.listdir(videofile)
    
    count = 0       ### start a counter at zero
    error = ''      ### error flag
    
    img = os.path.join(videofile, images[0])
    img = cv2.imread(img)
    
    tmp = skimage.color.rgb2gray(numpy.array(img))
    
    tmp = skimage.transform.downscale_local_mean(tmp, (5,5))

    ### create an array to save each image as an array as its loaded 
    i = 0;
    all_frames = []
    
    while i < len(images): ### while success == True
         ### if success is still true, attempt to read in next frame from vidcap video import
        count += 1  ### increase count
        frames = []  ### frames will be the individual images and frames_resh will be the "processed" ones
        try:
            slice_list = images[i:i+99]
        except:
            slice_list = images[i:]
            pass#print 'There are ', count, ' frame; delete last'        read_frames(videofile, name)
        for img in slice_list:
            img = os.path.join(videofile, img)
            img = cv2.imread(img)
            i += 1
            ### conversion from RGB to grayscale image to reduce data
            tmp = skimage.color.rgb2gray(numpy.array(img))
            ### ref for above: https://www.safaribooksonline.com/library/view/programming-computer-vision/9781449341916/ch06.html

            ### downsample image
            tmp = skimage.transform.downscale_local_mean(tmp, (5,5))
            frames.append(tmp)
            count+=99
        ### if the frames are the right shape (have 99 entries), then save
        #print numpy.shape(frames), numpy.shape(all_frames)
        if numpy.shape(frames)==(99, 144, 256):
            all_frames.append(frames)
        ### if not, pad the end with zeros
        elif numpy.shape(frames[0])==(144,256):
            #print shape(all_frames), shape(frames), shape(concatenate((all_frames[-1][-(99-len(frames)):], frames)))
            #print numpy.shape(all_frames), numpy.shape(frames)
            all_frames.append(numpy.concatenate((all_frames[-1][-(99-len(frames)):], frames)))
        elif numpy.shape(frames[0])!=(144,256):
            error = 'Video is not the correct resolution.'
    
    del frames;
    return all_frames, error


# In[18]:


# The data is then split (with the labels created above) into training and validation sets,
# with 60% of the total set as training and 20% as validation (the remaining 20% of data is
# left as a holdout test set).
# 
# The split fractions may look a little odd, but they are essentially ensuring that the validation
# and test sets are the same size (an overall 60-20-20 for training-validation-test).


import keras
from keras.models import Model
from keras.layers import Input, Dense, TimeDistributed
from keras.layers import LSTM

### set hyper-parameters
batch_size = 15
num_classes = 2
epochs = 30

### number of hidden layers in each NN
row_hidden = 128
col_hidden = 128

### get shape of rows/columns for each image
frame, row, col = (99, 144, 256)

### 4D input - for each 3-D sequence (of 2-D image) in each video (4th)
x = Input(shape=(frame, row, col))

encoded_rows = TimeDistributed(LSTM(row_hidden))(x)  ### encodes row of pixels using TimeDistributed Wrapper
encoded_columns = LSTM(col_hidden)(encoded_rows)     ### encodes columns of encoded rows using previous layer

### set up prediction and compile the model
prediction = Dense(num_classes, activation='softmax')(encoded_columns)
model = Model(x, prediction)


#### Checking the results - ROC curves

p = os.path.join(os.getcwd(), 'angelapp/modules/classification')
### first, load and compile the saved model to make predictions
model.load_weights(os.path.join(p, "HRNN_pretrained_model.hdf5"))
model.compile(loss='binary_crossentropy', optimizer='Nadam', metrics=['accuracy'])


# In[19]:


all_frames, err = load_set(os.path.join(os.getcwd(), 'angelapp/modules/classification', 'Data/Resize'))


# In[32]:


x = numpy.asarray(all_frames)
y = model.predict(x)


# In[33]:


print("Y: ", y)
print("yA: ", y[:,0], "\tAverage: ", numpy.mean(y[:,0]), "\tMax: ", max(y[:,0]))
print("yB: ", y[:,1], "\tAverage: ", numpy.mean(y[:,1]), "\tMax: ", max(y[:,1]))

with open(os.path.join(os.getcwd(), 'angelapp/modules/classification/Data/result.txt'), 'w+') as f:
    f.write('{}\n{}'.format(numpy.mean(y[:, 0]), numpy.mean(y[:, 1])))
try:
    shutil.rmtree(os.path.join(
        os.getcwd(), 'angelapp/modules/classification/Data/Extraction'))

    shutil.rmtree(os.path.join(
        os.getcwd(), 'angelapp/modules/classification/Data/Resize'))

except:
    pass

try:
    os.remove(os.path.join(os.getcwd(),  'angelapp/media/output.avi'))
except:
    pass