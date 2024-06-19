import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.layers import Flatten
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import tf2onnx
import onnx
from keras.layers import Dropout, Flatten
from PIL import Image
import parameters


np.random.seed(0)


#load the training data
Y_train = np.load('data/'+parameters.DATA_FOLDER+'/train/labels.npy')
X_train = []
for i in range(len(Y_train)):
    image=Image.open('data/'+parameters.DATA_FOLDER+'/train/'+str(i)+'.png')
    image= np.asarray(image)
    X_train.append(image)
X_train=np.array(X_train)


#load the validation data
Y_val = np.load('data/'+parameters.DATA_FOLDER+'/val/labels.npy')
X_val = []
for i in range(len(Y_val)):
    image=Image.open('data/'+parameters.DATA_FOLDER+'/val/'+str(i)+'.png')
    image= np.asarray(image)
    X_val.append(image)
X_val=np.array(X_val)


#define the preprocessing function for the input images: bring the value of every pixel from 0 to 1
def preprocess(img):
  img = img / 255
  return img

#apply the preprocessing function on the training and validation images
X_train = np.array(list(map(preprocess, X_train)))
X_val   = np.array(list(map(preprocess, X_val)))

#reshape the training and validation images
X_train = X_train.reshape(len(X_train), 32, 32, 1)
X_val = X_val.reshape(len(X_val), 32, 32, 1)


#perform data augmentation
datagen = ImageDataGenerator(width_shift_range = 0.1,height_shift_range = 0.1,zoom_range = 0.2,shear_range = 0.1,rotation_range = 10)
datagen.fit(X_train)
batches = datagen.flow(X_train, Y_train, batch_size = 20)
X_batch, y_batch = next(batches)


#transform the labels into categories
Y_train = keras.utils.to_categorical(Y_train, parameters.NB_CLASSES)
Y_val = keras.utils.to_categorical(Y_val, parameters.NB_CLASSES)


#define the neural network model
def leNet_model():
  model = Sequential()
  model.add(keras.layers.Conv2D(60, (5, 5), input_shape = (32, 32, 1), activation = 'relu'))
  model.add(keras.layers.Conv2D(60, (5, 5), activation = 'relu'))
  model.add(keras.layers.MaxPooling2D(pool_size = (2, 2)))
  
  model.add(keras.layers.Conv2D(30, (3, 3), activation = 'relu'))
  model.add(keras.layers.Conv2D(30, (3, 3), activation = 'relu'))
  model.add(keras.layers.MaxPooling2D(pool_size = (2, 2)))
  model.add(Dropout(0.5))
  
  model.add(Flatten())
  model.add(Dense(500, activation = 'relu'))
  model.add(Dropout(0.5))
  model.add(Dense(2, activation = 'softmax'))
  model.compile(Adam(lr = 0.001), loss = 'categorical_crossentropy', metrics = ['accuracy'])

  return model

model = leNet_model()


#train the model
history = model.fit(datagen.flow(X_train, Y_train, batch_size = 50), steps_per_epoch = 10, epochs = 20, validation_data = (X_val, Y_val), shuffle = 1)


#save the model into a .onnx and a .keras
keras.models.save_model(model,parameters.NAME_OUTPUT_FILE+'.keras')
input_signature = [tf.TensorSpec([None,32,32,1], tf.float32, name='x')]
onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature, opset=13)
onnx.save(onnx_model, parameters.NAME_OUTPUT_FILE+'.onnx')