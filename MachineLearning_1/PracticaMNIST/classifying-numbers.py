#!/usr/bin/env python
# coding: utf-8

# In[1]:


import keras
keras.__version__


# # Introduction to ConvNets: Classifying handwritten numbers
# 
# 
# Let's take a look at a simple example of a convnet. We will use it to classify the MNIST dataset, which is an open dataset containing handwritten numbers. 
# 
# ![Handwritten numbers from the MNIST dataset](http://corochann.com/wp-content/uploads/2017/02/mnist_plot.png)
# 
# Let's create a first basic convnet. It's a stack of 'Conv2D' and 'MaxPooling2D' layers. 
# The important thing to note is that a convnet takes as input tensors of size `(image_height, image_width, image_channels)`. 
# To do this we must first find out the size of the images in our dataset. 
# 
# The network must have the following layers:
# 
# - A convolutional layer (Conv2D) with 32 3x3 filters and relu activation. In this first layer you must indicate the size of the input (input_shape).
# - A second layer of Max Pooling (MaxPooling2D) of 2x2
# - A third convolutional layer with 64 3x3 filters and relu activation
# - A fourth layer of 2x2 Max Pooling (MaxPooling2D)
# - A fifth convolutional layer of 64 3x3 filters and relu activation
# 
# You'll know you've done it right when the model.summary() output is:
# 
# ![imagen_output.png](https://github.com/laramaktub/MachineLearningI/blob/master/imagen_output.png?raw=true)
# 

# In[2]:


from keras import layers
from keras import models

model = models.Sequential()

model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)))
model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None))

model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None))

model.add(layers.Conv2D(64, (3,3), activation='relu'))

model.summary()


# You can see above that the output of each Conv2D and MaxPooling2D layer is a 3D tensor of dimensions (height, width, channels). The width and height tend to decrease as we go deeper into the network. The number of channels is controlled by the first argument passed to the Conv2D layers (e.g. 32 or 64).
# 
# The next step would be to give our last tensor (of dimensions (3, 3, 64)) as input to a densely connected network. These classifiers process vectors, which are 1D, while our output is a 3D tensor. So first we will have to flatten our 3D output and convert it to 1D and then add a few dense layers:
# 
# - First flatten the output.
# - Add a first layer of 64 neurons and relu activation
# - Add a last layer of 10 neurons (as many as you can sort) and softmax activation
# - You'll know you've done well when the summary looks like this:
# 
# ![imagen_output_flat.png](https://github.com/laramaktub/MachineLearningI/blob/master/imagen_output_flat.png?raw=true)

# In[3]:


model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.summary()


# As you can see, our dimensional output `(3, 3, 64)` has been flattened into a vector of dimension `(576,)`, before entering the two dense layers.
# 
# We are now going to train our network with the images from the MNIST dataset.
# 
# We then load the dataset and put it into vectors: train_images, train_labels, test_images, test_labels
# 
# Before you continue, print:
# 
# - What is the size of the training dataset?
# - What does the training dataset look like?
# - What do the training labels look like?
# - Print the fourth image of the training dataset
# 

# In[4]:


from keras.datasets import mnist
from keras.utils import to_categorical

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

print("The size of the training dataset is:", len(train_images))

# Pinto las primeras imagenes
from matplotlib import pyplot

for i in range(8):
    # define subplot
    pyplot.subplot(240 + 1 + i)
    # plot raw pixel data
    pyplot.imshow(train_images[i], cmap=pyplot.get_cmap('gray'))
    labels = "label = " + str(train_labels[i])
    pyplot.title(labels)
# show the figure
pyplot.show()


# Next you will give the appropriate shape to the training and test datasets in order to put them into the neural network. Convert the labels, which right now are numbers, into their categorical form.

# In[5]:


train_images = train_images.reshape((60000, 28, 28, 1))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images.astype('float32') / 255

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)


# In[6]:


for i in range(8):
    print(train_labels[i])


# Compile the model indicating what the training data and its labels are. Using the optimizer "rmsprop" and as a loss function use the categorical cross entropy.
# Then train the model for 5 epochs and a batch size of 64.

# In[7]:


model.compile(optimizer = "rmsprop", 
              loss = "categorical_crossentropy", 
              metrics=['accuracy'])


# In[8]:


model.fit(x = train_images, 
          y = train_labels,
          batch_size=4,
          epochs=5)


# Let's evaluate the model with the test images:

# In[9]:


test_loss, test_acc = model.evaluate(test_images, test_labels, verbose = 0)
print('Test loss:', test_loss)
print('Test accuracy:', test_acc)


# Create an image with a handwritting number and check the prediction. Try with several numbers ...does it work properly?

# In[17]:


from keras.preprocessing import image
import numpy as np
from matplotlib import pyplot as plt

img_width=28
img_height=28

img = image.load_img('cuatro.png', target_size=(img_width, img_height), color_mode = "grayscale")
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)

# Pinto mi nueva imagen de un numero
x_to_plot = np.reshape(x, (28,-1))
pyplot.subplot(240 + 1)
pyplot.imshow(x_to_plot, cmap=pyplot.get_cmap('gray'))
pyplot.show()


# In[18]:


# Veo como se clasifica
y = model.predict_classes(x)
print(y[0])


# In[19]:


model.save('net_numbers.h5')


# Load the model that you just saved and make a prediction (predict_classes) with the number you just generated. 
# 

# In[20]:


from keras.models import load_model
loaded_model = load_model('net_numbers.h5')

# miro si de verdad estoy cargando el modelo que he guardado antes 
loaded_model.summary()

test_loss, test_acc = loaded_model.evaluate(test_images, test_labels, verbose = 0)
print('Test loss:', test_loss)
print('Test accuracy:', test_acc)


# In[21]:


from keras.preprocessing import image
import numpy as np
from matplotlib import pyplot as plt

img_width=28
img_height=28

img = image.load_img('tres.png', target_size=(img_width, img_height), color_mode = "grayscale")
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)

x_to_plot = np.reshape(x, (28,-1))
pyplot.subplot(240 + 1)
pyplot.imshow(x_to_plot, cmap=pyplot.get_cmap('gray'))
pyplot.show()

y = loaded_model.predict_classes(x)
print("Lo reconozco como un", y[0])

# No muy bien, la verdad ...


# In[22]:


# Miro que pasa con las imagenes originales de test: mucho mejor
j = 100

pyplot.subplot(240 + 1)
test_image_to_plot = np.reshape(test_images[j], (28,-1))

pyplot.imshow(test_image_to_plot, cmap=pyplot.get_cmap('gray'))
labels = "label = " + str(test_labels[j])
pyplot.title(labels)

test_image = np.expand_dims(test_images[j], axis=0)
y = loaded_model.predict_classes(test_image)
print("Lo reconozco como un", y[0])

