import numpy as np
import matplotlib.pyplot as plt
import keras
from PIL import Image

np.random.seed(0)


#load the model
model=keras.models.load_model('model2.keras')


#find and preprocesses the image
img = Image.open('noisy.png')
plt.imshow(img, cmap=plt.get_cmap('gray'))
plt.show()
img = np.asarray(img)
img = img.reshape(1, 32, 32, 1)


#compute and print the class
class_scores = model.predict(img)
predicted_class = np.argmax(class_scores, axis=1)[0]
print('Predicted class for the tested image is: ',predicted_class)