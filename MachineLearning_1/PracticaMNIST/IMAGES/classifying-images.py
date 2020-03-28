#!/usr/bin/env python
# coding: utf-8

# In[1]:


import keras
keras.__version__


# # Using convnets with small datasets
# 
# The first thing to do is download the following file https://lara.web.cern.ch/lara/train.zip in the jupyter terminal and uncompress it in the same folder as this notebook. 
# 
# To download another dataset from imagenet you can do it with the URL list of the images and using `wget -i`
# 
# 
# 
# ## Training a convnet from scratch
# 
# Training an image classification model with very little data is a common situation you will find yourself in if you end up doing Computer Vision in a professional context.  
# 
# Having "few" samples can mean anything from a few hundred to a few tens of thousands of images.  Let's illustrate a practical example here: let's focus on classifying images as "dogs" and "cats". 
# 

# ## The importance of DEEP Learning in problems with few data
# 
# You may have heard many times that Deep Learning only works when you have large amounts of data. This is partly true: one of the characteristics of Deep learning is that you can find interesting features from the training dataset itself, and this a priori is easier when you have many examples available, especially in the case of having input datasets with a high dimensionality, such as images.
# 
# However, what constitutes a "large" dataset is relative. Specifically relative to the size and depth of the network we are trying to train. It is not possible to sand a convnet so that it becomes a complete problem with only a few dozen examples, but a few hundred can be enough if the model is well assembled (we will understand what "well assembled" means throughout the Deep Learning course).
# 
# Since convnets learn local characteristics, invariant under translations, they are very efficient in terms of the number of images needed to carry out perceptual problems. So training a convnet from 0 with a not very large dataset can still lead to reasonable results as we will see here.
# 
# But there is more: Deep Learning models are highly "recyclable". One can, for example, take an image classification problem and a trained speech-to-text converter on a very big dataset and then reuse it for solving a completely different problem only by adding some small modifications. More specifically, in the case of Computer Vision, many pre-trained models (usually trained on the ImageNet dataset) are made public so that one can download them and use them to create powerful Computer Vision models with very little data.
# 
# But here we will just run a simple example.
#  
# 

# ## Los datos
# 
# The cat vs dog dataset we use is not a Keras package. It was posted on Kaggle.com as part of a Computer Vision problem in late 2013, when ConvNets were not yet so popular. 
# 
# The images are medium resolution JPGEs. It looks like this:
# 
# ![cats_vs_dogs_samples](https://s3.amazonaws.com/book.keras.io/img/ch5/cats_vs_dogs_samples.jpg)

# It's no surprise that the 2013 Kaggle cat vs dog competition was won by ConvNets. The best were able to achieve up to 95% accuracy. In our example we are still far from this accuracy, but during the Deep Learning course we have learned how to approach this value using different methods to improve the performance of neural networks. It should be noted that in this example we are training on approximately only 10% of the data that was used for the contest. 
# After downloading the dataset and decompressing it, we are going to create a new dataset containing three subsets: a training set containing 1000 images of each class, a validation set with 500 images of each class, and finally a test set with 500 images of each class.
# 
# Here we have a few lines of code that make us this distribution automatically:
# 
# 
# 

# In[2]:


import os, shutil


# In[3]:


# The path to the directory where the original
# dataset was uncompressed
original_dataset_dir = '/home/nicolo/DataScienceMaster/MachineLearning_1/PracticaMNIST/train'

# The directory where we will
# store our smaller dataset
base_dir = '/home/nicolo/DataScienceMaster/MachineLearning_1/PracticaMNIST/cats_and_dogs_small'
#os.mkdir(base_dir, )

# Directories for our training,
# validation and test splits
train_dir = os.path.join(base_dir, 'train')
#os.mkdir(train_dir)
validation_dir = os.path.join(base_dir, 'validation')
#os.mkdir(validation_dir)
test_dir = os.path.join(base_dir, 'test')
#os.mkdir(test_dir)

# Directory with our training cat pictures
train_cats_dir = os.path.join(train_dir, 'cats')
#os.mkdir(train_cats_dir)

# Directory with our training dog pictures
train_dogs_dir = os.path.join(train_dir, 'dogs')
#os.mkdir(train_dogs_dir)

# Directory with our validation cat pictures
validation_cats_dir = os.path.join(validation_dir, 'cats')
#os.mkdir(validation_cats_dir)

# Directory with our validation dog pictures
validation_dogs_dir = os.path.join(validation_dir, 'dogs')
#os.mkdir(validation_dogs_dir)

# Directory with our validation cat pictures
test_cats_dir = os.path.join(test_dir, 'cats')
#os.mkdir(test_cats_dir)

# Directory with our validation dog pictures
test_dogs_dir = os.path.join(test_dir, 'dogs')
#os.mkdir(test_dogs_dir)

# Copy first 1000 cat images to train_cats_dir
fnames = ['cat.{}.jpg'.format(i) for i in range(1000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(train_cats_dir, fname)
    shutil.copyfile(src, dst)

# Copy next 500 cat images to validation_cats_dir
fnames = ['cat.{}.jpg'.format(i) for i in range(1000, 1500)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(validation_cats_dir, fname)
    shutil.copyfile(src, dst)
    
# Copy next 500 cat images to test_cats_dir
fnames = ['cat.{}.jpg'.format(i) for i in range(1500, 2000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(test_cats_dir, fname)
    shutil.copyfile(src, dst)
    
# Copy first 1000 dog images to train_dogs_dir
fnames = ['dog.{}.jpg'.format(i) for i in range(1000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(train_dogs_dir, fname)
    shutil.copyfile(src, dst)
    
# Copy next 500 dog images to validation_dogs_dir
fnames = ['dog.{}.jpg'.format(i) for i in range(1000, 1500)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(validation_dogs_dir, fname)
    shutil.copyfile(src, dst)
    
# Copy next 500 dog images to test_dogs_dir
fnames = ['dog.{}.jpg'.format(i) for i in range(1500, 2000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(test_dogs_dir, fname)
    shutil.copyfile(src, dst)


# As a sanity check, let's count how many pictures we have in each training split (train/validation/test):

# In[4]:


print('total training cat images:', len(os.listdir(train_cats_dir)))


# In[5]:


print('total training dog images:', len(os.listdir(train_dogs_dir)))


# In[6]:


print('total validation cat images:', len(os.listdir(validation_cats_dir)))


# In[7]:


print('total validation dog images:', len(os.listdir(validation_dogs_dir)))


# In[8]:


print('total test cat images:', len(os.listdir(test_cats_dir)))


# In[9]:


print('total test dog images:', len(os.listdir(test_dogs_dir)))


# So effectively we have 2000 training images, 1000 validation images and 1000 test images. In each of these subsets there are the same number of examples from each class: this is what is called a balanced binary classification system, which means that our classification accuracy will be an adequate metric of the success of our solution.

# ## Building our network
# 
# In the above example we have built a small convnet to solve the problem of classifying handwritten numbers using the MNIST dataset, so we are already familiar with the terminology that keras uses. We are going to reuse the general structure we had in the previous example: our convnet will have a stack of alternate layers of `Conv2D` (with `relu` activation) and `MaxPooling2D` layers.
# 
# However, since we are dealing with larger images and a more complex problem, we will create our network accordingly: it will have one more layer of `Conv2D` + `MaxPooling2D`. This serves to increase the capacity of the network and to further reduce the size of the feature maps, so that they are not so huge when they reach the flattening step. We start using 150x150 input images (an arbitrary choice), and end up with feature maps that are 7x7 in size before the flattening layer.
# 
# It is important to note that the depth of feature maps progressively increases as we move through the neural network (from 32 to 128) while the size of feature maps decreases (from 148x148 to 7x7). You will see this pattern in almost all convnets.
# 
# As we are attacking a binary classification problem (dog or cat), we are going to finish the network with a single unit (a dense layer of size 1) and with a sigmoid activation. This unit will encode the probability that our network is looking at one class or another.
# 
# The final look of the model should be as follows:
# 
# 
# ![modelo_red_animales.png](https://github.com/laramaktub/MachineLearningI/blob/master/modelo_red_animales.png?raw=true)

# In[ ]:


from keras import layers
from keras import models

model = models.Sequential()

model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(150,150,3)))
model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None))

model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None))

model.add(layers.Conv2D(128, (3,3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None))

model.add(layers.Conv2D(128, (3,3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None))

model.add(layers.Flatten())

model.add(layers.Dense(512, activation='relu'))

model.add(layers.Dense(1, activation='sigmoid'))

model.summary()


# Para el paso de compilación utilizaremos el optimizador `RMSprop`(lr=1e-4). Como nuestra red termina con una única unidad sigmoide, vamos a utilizar binary crossentropy como nuestra función de pérdida.

# In[ ]:


from keras import optimizers

rms = optimizers.RMSprop(lr=1e-4)

model.compile(optimizer = rms, #'rmsprop', 
              loss = "binary_crossentropy", 
              metrics=['acc'])


# ##  Data preprocessing
# 
# The images must be properly formatted as float tensors before they are given to the net. That's just what we're going to do here. Before we pre-process them, the images are JPEG files. The steps to be able to give them to our network are roughly as follows:
# 
# * Read the files with the images.
# * Decode the content of the JPEG in a "grid" with the RGB of the pixels 
# * Turn that "grill" into floatation devices
# * Rescale the pixel values (between 0 and 255) to the [0, 1] interval as neural networks prefer to work with small values. 
# 
# All this may seem very complicated but thanks to Keras our life is much easier and we can count on your tools to take care of these steps automatically. Keras has a module with tools for image processing, which can be found in `keras.preprocessing.image`. In particular, it contains the class `ImageDataGenerator` that allows us to automatically convert images we have on the hard disk into pre-processed tensors. This is exactly what we'll be using next. To do this we can use the flow_from_directory to take the images directly from the folders that we previously generated. We give it as input the folders where the training (or validation) images are, the size of the images (target_size), the size of the batch we're going to use (we're going to start with 20) and as there are only two categories, we tell it that we're going to use binary_crossentropy (class_mode). When we run these commands we'll get the following, the total number of images and how many classes there are.

# In[10]:


from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=(150, 150),
                                                    batch_size=20,
                                                    class_mode='binary')

test_generator = test_datagen.flow_from_directory(test_dir,
                                                  target_size=(150, 150),
                                                  batch_size=20,
                                                  class_mode='binary')

validation_generator = validation_datagen.flow_from_directory(validation_dir,
                                                              target_size=(150, 150),
                                                              batch_size=20,
                                                              class_mode='binary')


# Let's take a look at one of these generators: it takes us to a batch of 150x150 RGB images (dimensions `(20, 150, 150, 3)`) and binary tags (dimension `(20,)`). 20 is the number of examples in each batch (what we call the batch size). The generator generates these batches indefinitely: it runs a loop endlessly through all the images we have in the folder. That's why we have to type `break` to break the loop at some point.
# 

# In[ ]:


for data_batch, labels_batch in train_generator:
    print('data batch shape:', data_batch.shape)
    print('labels batch shape:', labels_batch.shape)
    break


# Now let's make the fit. In this case, as what we have is a generator, we use fit_generator. We are going to run 30 epochs and use the validation dataset.

# In[ ]:


history = model.fit_generator(train_generator,
                              epochs = 30,
                              validation_data = validation_generator)


# It's a nice idea to save the model after training

# In[27]:


model.save('net_images.h5')


# Let's now evaluate our model using the test dataset

# In[28]:


# Cargo el modelo, ya que lo he guardado

from keras.models import load_model
loaded_model = load_model('net_images.h5')

# miro si de verdad estoy cargando el modelo que he guardado antes 
loaded_model.summary()

test_loss, test_acc = loaded_model.evaluate(test_generator, verbose = 0)
print('Test loss:', test_loss)
print('Test accuracy:', test_acc)


# Try to optimize the network with the tools you have learnt during the lesson. Try to make improvements both in terms of speed and accuracy. Comment the results. 

# ### Intento mejorar el resultado

# Tratandose de un dataset con pocas imagenes, voy a intentar utilizar técnicas de data augmentation para que la red tenga más eventos para entrenar:
# - horizontal flip;
# - vertical flip;
# - rotation;
# - zoom
# 
# Intento usar un learning rate más alto, para acercarme al mejor valor de la accuracy más rápidamente.

# In[20]:


from keras.preprocessing.image import ImageDataGenerator

train_datagen2 = ImageDataGenerator(rescale=1./255,
                                  horizontal_flip=True,
                                  vertical_flip=True,
                                  rotation_range=90,
                                  zoom_range=[0.5,1.0])

test_datagen2 = ImageDataGenerator(rescale=1./255,
                                 horizontal_flip=True,
                                 vertical_flip=True,
                                 rotation_range=90,
                                 zoom_range=[0.5,1.0])

validation_datagen2 = ImageDataGenerator(rescale=1./255,
                                       horizontal_flip=True,
                                       vertical_flip=True,
                                       rotation_range=90,
                                       zoom_range=[0.5,1.0])

train_generator2 = train_datagen2.flow_from_directory(train_dir,
                                                    target_size=(150, 150),
                                                    batch_size=20,
                                                    class_mode='binary')

test_generator2 = test_datagen2.flow_from_directory(test_dir,
                                                  target_size=(150, 150),
                                                  batch_size=20,
                                                  class_mode='binary')

validation_generator2 = validation_datagen2.flow_from_directory(validation_dir,
                                                              target_size=(150, 150),
                                                              batch_size=20,
                                                              class_mode='binary')


# In[21]:


from keras.layers import Dense, Dropout, Activation, Flatten
from keras import layers
from keras import models
from keras import regularizers

model2 = models.Sequential()

model2.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(150,150,3)))
model2.add(layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None))

model2.add(layers.Conv2D(64, (3,3), activation='relu'))
model2.add(layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None))

model2.add(layers.Conv2D(128, (3,3), activation='relu'))
model2.add(layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None))

model2.add(layers.Conv2D(128, (3,3), activation='relu'))
model2.add(layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None))

model2.add(layers.Flatten())

model2.add(layers.Dense(512, activation='relu'))

model2.add(layers.Dense(1, activation='sigmoid'))

model2.summary()


# In[22]:


from keras import optimizers
from keras.callbacks import EarlyStopping
              
rms = optimizers.RMSprop(lr=5e-4)

es = EarlyStopping(monitor='val_acc', mode='max', patience = 5,
                  restore_best_weights = True)

model2.compile(optimizer = rms,             
               loss = "binary_crossentropy", 
               metrics=['acc'])


# In[23]:


history2 = model2.fit_generator(train_generator2,
                                epochs = 30,
                                validation_data = validation_generator2,
                                callbacks = [es])


# In[25]:


# Miro la accuracy en el test
test_loss2, test_acc2 = model2.evaluate(test_generator2, verbose = 0)
print('Test loss:', test_loss2)
print('Test accuracy:', test_acc2)


# In[26]:


model2.save('my_net_images.h5')

