import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import keras
import parameters

np.random.seed(0)


#load the model
model=keras.models.load_model(parameters.NAME_OUTPUT_FILE+'.keras')


#load the test data
Y_test = np.load('data/'+parameters.DATA_FOLDER+'/test/labels.npy')
X_test = []
for i in range(len(Y_test)):
    image=Image.open('data/'+parameters.DATA_FOLDER+'/test/'+str(i)+'.png')
    image= np.asarray(image)
    X_test.append(image)
X_test=np.array(X_test)


#define the preprocessing function for the input images: bring the value of every pixel from 0 to 1
def preprocess(img):
  img = img / 255
  return img


#apply the preprocessing function on the test images
X_test  = np.array(list(map(preprocess, X_test)))


#reshape the test images
X_test = X_test.reshape(len(X_test), 32, 32, 1)


#transform the labels into categories
Y_test = keras.utils.to_categorical(Y_test, parameters.NB_CLASSES)


#compute the predictions of the model for the test data
Y_prediction = model.predict(X_test)
Y_prediction = np.argmax (Y_prediction, axis = 1)
Y_test=np.argmax(Y_test, axis=1)


#create and plot the confusion matrix
cm = confusion_matrix(Y_test, Y_prediction , normalize='pred')
disp = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=[0,1])
disp.plot()
plt.show()