# -*- coding: utf-8 -*-
"""Food and NonFood_ Deep Learning _Transfer Learning _VGG19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OEqnVE_GODFkJoY3YpztEG5Jo7Pfj0NM
"""

! pip install tensorflow-gpu

! pip install keras

! pip install pandas

import matplotlib.pylab as plt
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
print("TF version:", tf.__version__)
print("Hub version:", hub.__version__)
print("GPU is", "available" if tf.test.is_gpu_available() else "NOT AVAILABLE")

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
#from tensorflow.keras.applications.resnet50 import ResNet50
#from tensorflow.keras.applications.resnet152V2 import ResNet152V2
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
from glob import glob
#from keras.applications.inception_v3 import InceptionV3
#from keras.applications.inception_v3 import preprocess_input, decode_predictions

from sklearn.utils import shuffle
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score
import os
import cv2

from google.colab import drive
drive.mount('/content/drive')

train_X = []
train_y = []
IMG_SIZE = 224
DIR1 = "/content/drive/My Drive/Colab Notebooks/Food and NotFood/training/"
train_data = os.listdir(DIR1)
train_data

for file in train_data:
    filename = os.path.join(DIR1, file)
    if file=='Non-Food':
      label=0
    else:
      label=1
    print("Folder {} started".format(file))
    try:
        for img in os.listdir(filename):
            path = os.path.join(filename, img)
            img = cv2.imread(path,cv2.IMREAD_COLOR)
            img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))

            train_X.append(np.array(img))
            train_y.append(label)
    except:
        print("File {} not read".format(path))
        
    print("Folder {} done".format(file))
    print("The folder {} is labeled as {}".format(file, label))

test_X = []
test_y = []
IMG_SIZE = 224
DIR2 = "/content/drive/My Drive/Colab Notebooks/Food and NotFood/validation/"
test_data = os.listdir(DIR2)
test_data

for file in test_data:
    filename = os.path.join(DIR2, file)
    if file=='Non-Food':
      label=0
    else:
      label=1
    print("Folder {} started".format(file))
    try:
        for img in os.listdir(filename):
            path = os.path.join(filename, img)
            img = cv2.imread(path,cv2.IMREAD_COLOR)
            img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))

            test_X.append(np.array(img))
            test_y.append(label)
    except:
        print("File {} not read".format(path))
        
    print("Folder {} done".format(file))
    print("The folder {} is labeled as {}".format(file, label))

eval_X = []
eval_y = []
IMG_SIZE = 224
DIR3 = "/content/drive/My Drive/Colab Notebooks/Food and NotFood/evaluation/"
eval_data = os.listdir(DIR3)
eval_data

for file in eval_data:
    filename = os.path.join(DIR3, file)
    if file=='Non-Food':
      label=0
    else:
      label=1
    print("Folder {} started".format(file))
    try:
        for img in os.listdir(filename):
            path = os.path.join(filename, img)
            img = cv2.imread(path,cv2.IMREAD_COLOR)
            img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))

            eval_X.append(np.array(img))
            eval_y.append(label)
    except:
        print("File {} not read".format(path))
        
    print("Folder {} done".format(file))
    print("The folder {} is labeled as {}".format(file, label))

import random
from random import sample
plt.figure(figsize=(10,10))
random_indexes = sample(range(1, 3000), 10)
print(random_indexes)
for i, img_index in enumerate(random_indexes):

  # Set up subplot; subplot indices start at 1
  sp = plt.subplot(6,2, i + 1)
  sp.set_title(train_data[train_y[img_index]])
  sp.axis('Off') # Don't show axes (or gridlines)
  plt.imshow(train_X[img_index])

random_state = 100
train_X, train_y = shuffle(train_X, train_y, random_state = random_state)
test_X, test_y = shuffle(test_X, test_y, random_state = random_state)
eval_X, eval_y = shuffle(eval_X, eval_y, random_state = random_state)

train_X = np.array(train_X)
train_y = np.array(train_y)

test_X = np.array(test_X)
test_y = np.array(test_y)

eval_X = np.array(eval_X)
eval_y = np.array(eval_y)

print("train_X shape is {}".format(train_X.shape))
print("train_y shape is {}".format(train_y.shape))

print('\n')

print("test_X shape is {}".format(test_X.shape))
print("test_y shape is {}".format(test_y.shape))

print('\n')

print("eval_X shape is {}".format(eval_X.shape))
print("eval_y shape is {}".format(eval_y.shape))

from tensorflow.keras.utils import to_categorical

print("Before the categorical the shape of train_y is {}".format(train_y.shape))
train_y = to_categorical(train_y)
print("After the categorical the shape of train_y is {}".format(train_y.shape))

print('\n')

print("Before the categorical the shape of test_y is {}".format(test_y.shape))
test_y = to_categorical(test_y)
print("After the categorical the shape of test_y is {}".format(test_y.shape))

print('\n')

print("Before the categorical the shape of eval_y is {}".format(eval_y.shape))
eval_y = to_categorical(eval_y)
print("After the categorical the shape of eval_y is {}".format(eval_y.shape))

training_datagen = ImageDataGenerator(
      rescale = 1./255,
      rotation_range=40,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest')


validation_datagen = ImageDataGenerator(
      rescale = 1./255)

evaluation_datagen = ImageDataGenerator(
      rescale = 1./255)

training_set=training_datagen.flow(train_X,train_y)
test_set=validation_datagen.flow(test_X,test_y)
eval_set=evaluation_datagen.flow(eval_X,eval_y)

# Import the InceptionV3 library as shown below and add preprocessing layer to the front of InceptionV3",
# Here we will be using imagenet weights\n"
IMAGE_SIZE=[224,224]
vgg= VGG19(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# don't train existing weights\n",
for layer in vgg.layers:
    layer.trainable = False

folders = glob('/content/drive/My Drive/Colab Notebooks/Food and NotFood/training/*')
len(folders)

x = Flatten()(vgg.output)

prediction=Dense(len(folders), activation='softmax')(x)

model = Model(inputs=vgg.input, outputs=prediction)

model.summary()

model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

batch_size=32
r= model.fit_generator(training_set,epochs = 10, validation_data = test_set,verbose = 1, steps_per_epoch=train_X.shape[0] // batch_size,validation_steps=test_X.shape[0] // batch_size)

# plot the loss
plt.figure(figsize=(10,6))

plt.subplot(1,2,1)
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.savefig('LossVal_loss')

# plot the accuracy
plt.subplot(1,2,2)
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.savefig('AccVal_acc')

k=r.history['val_accuracy']
print('The Validation Accuracy of VGG19 Model: ', np.mean(k))

# save it as a h5 file

from tensorflow.keras.models import load_model
model.save('Food_model_vgg19.h5')

y_pred = model.predict(test_X)
y_pred_digits = np.argmax(y_pred, axis=1)
y_pred_digits

y_pred_labels = np.unique(y_pred_digits, return_counts=True)
y_pred_labels

real_labels= np.argmax(test_y, axis=1)
real_labels
real_labels1 = np.unique(real_labels, return_counts=True)
real_labels1

from sklearn.metrics import confusion_matrix
c_m = confusion_matrix(real_labels, y_pred_digits)
c_m

import seaborn as sns
plt.figure(figsize = (6,6))
sns.heatmap(c_m,cmap= "Reds", linecolor = 'black' , linewidth = 1 , annot = True, fmt='' , xticklabels = train_data , yticklabels = train_data)
plt.xlabel('Predicted')
plt.ylabel('Actual')

from sklearn.metrics import confusion_matrix,roc_curve,auc,accuracy_score
acc_score = accuracy_score(real_labels, y_pred_digits)
acc_score

# now storing some properly as well as misclassified indexes'.
i=0
prop_class=[]
mis_class=[]

for i in range(len(real_labels)):
    if(real_labels[i] == y_pred_digits[i]):
        prop_class.append(i)
    if(len(prop_class)==10):
        break
i=0
for i in range(len(real_labels)):
    if(real_labels[i] != y_pred_digits[i]):
        mis_class.append(i)

print(len(mis_class))

labels_names={0:'Non-Food', 
        1:'Food'
        }
#fig.set_size_inches(8,8)
import random
from random import sample
plt.figure(figsize=(18,18))
random_indexes = sample(range(0, 10), 10)
print(random_indexes)
for i, img_index in enumerate(random_indexes):

  # Set up subplot; subplot indices start at 1
  sp = plt.subplot(5, 2, i + 1)
  sp.set_title('Actual Bird: '+ labels_names[real_labels[prop_class[img_index]]]+ '\n' + 'Predicted Bird : ' + labels_names[y_pred_digits[prop_class[img_index]]])
  sp.axis('Off') # Don't show axes (or gridlines)
  plt.imshow(test_X[prop_class[img_index]])

labels_names={0:'Non-Food', 
        1:'Food'
        }
import random
from random import sample

random_indexes = sample(range(0, 10), 10)
print(random_indexes)
plt.figure(figsize=(25,25))
for i, img_index in enumerate(random_indexes):
  # Set up subplot; subplot indices start at 1
  sp = plt.subplot(5, 2, i + 1)
  sp.set_title('Actual Bird: '+ labels_names[real_labels[mis_class[img_index]]]+ '\n' + 'Predicted Bird : ' + labels_names[y_pred_digits[mis_class[img_index]]])
  sp.axis('Off') # Don't show axes (or gridlines)
  plt.imshow(test_X[mis_class[img_index]])

# Evaluate The Model with Different Images

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model=load_model('Food_model_vgg19.h5')

eval_y_pred = model.predict(eval_X)
eval_y_pred_digits = np.argmax(eval_y_pred, axis=1)
eval_y_pred_digits

eval_y_pred_labels = np.unique(eval_y_pred_digits, return_counts=True)
eval_y_pred_labels

eval_real_labels= np.argmax(eval_y, axis=1)
eval_real_labels

eval_real_labels1 = np.unique(eval_real_labels, return_counts=True)
eval_real_labels1

from sklearn.metrics import confusion_matrix
c_m1 = confusion_matrix(eval_real_labels, eval_y_pred_digits)
c_m1

labelss=['Non-Food', 'Food']
import seaborn as sns
plt.figure(figsize = (6,6))
sns.heatmap(c_m1,cmap= "Reds", linecolor = 'black' , linewidth = 1 , annot = True, fmt='' , xticklabels = labelss , yticklabels = labelss)
plt.xlabel('Predicted')
plt.ylabel('Actual')



results = model.evaluate(eval_X, eval_y, batch_size=32)
print("test loss, test acc:", results)



img=image.load_img('/content/drive/My Drive/Colab Notebooks/noodles.jpg',target_size=(224,224))

img

y=image.img_to_array(img)
y=np.expand_dims(y,axis=0)
imgy=preprocess_input(y)
imgy=imgy/255

preds= model.predict(imgy)
preds

a=np.argmax(preds, axis=1)
a

if(a==0):
    print("Non-Food")
else:
    print("Food")

