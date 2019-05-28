
from __future__ import absolute_import, division, print_function
import os
import numpy as np
import PIL.Image as Image
import matplotlib.pylab as plt
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers
from tensorflow.keras import backend as K

#Locate image data
data_root = 'images/train_set'
image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
image_data = image_generator.flow_from_directory(data_root)

#get pretrained classifier
feature_extractor_url = 'https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/3'
def feature_extractor(x):
    feature_extractor_module = hub.Module(feature_extractor_url)
    return feature_extractor_module(x)
IMAGE_SIZE = hub.get_expected_image_size(hub.Module(feature_extractor_url))

#Image data
image_data = image_generator.flow_from_directory(str(data_root), target_size=IMAGE_SIZE)
for image_batch,label_batch in image_data:
  print("Image batch shape: ", image_batch.shape)
  print("Label batch shape: ", label_batch.shape)
  break

#Create model
features_extractor_layer = layers.Lambda(feature_extractor, input_shape=IMAGE_SIZE+[3])
features_extractor_layer.trainable = False
model = tf.keras.Sequential([
    features_extractor_layer,
    layers.Dense(image_data.num_classes, activation='softmax')
])
model.summary()

#Intialize training session
sess = K.get_session()
init = tf.global_variables_initializer()
sess.run(init)

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

class CollectBatchStats(tf.keras.callbacks.Callback):
  def __init__(self):
    self.batch_losses = []
    self.batch_acc = []
    
  def on_batch_end(self, batch, logs=None):
    self.batch_losses.append(logs['loss'])
    self.batch_acc.append(logs['acc'])

#Train
steps_per_epoch = image_data.samples//image_data.batch_size
batch_stats = CollectBatchStats()
model.fit((item for item in image_data), epochs=10, 
                    steps_per_epoch=steps_per_epoch,
                    callbacks = [batch_stats])

#Get label names
label_names = sorted(image_data.class_indices.items(), key=lambda pair:pair[1])
label_names = np.array([key.title() for key, value in label_names])
label_names

#Get predictions
result_batch = model.predict(image_batch)

labels_batch = label_names[np.argmax(result_batch, axis=-1)]
labels_batch

#Visualize predictions
plt.figure(figsize=(10,9))
for n in range(30):
  plt.subplot(6,5,n+1)
  plt.imshow(image_batch[n])
  plt.title(labels_batch[n])
  plt.axis('off')
_ = plt.suptitle("Model predictions")

#Save model
if not os.path.exists('models'):
    os.makedirs('models')
saver = tf.train.Saver()
saver.save(sess, 'models/my_model')

#Testing the model
#Locate test images
data_root = 'images/test_set'
image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
image_data = image_generator.flow_from_directory(data_root)
image_data = image_generator.flow_from_directory(str(data_root), target_size=IMAGE_SIZE)
for image_batch,label_batch in image_data:
  print("Image batch shape: ", image_batch.shape)
  print("Label batch shape: ", label_batch.shape)
  break
result_batch = model.predict(image_batch)
labels_batch = label_names[np.argmax(result_batch, axis=-1)]
labels_batch

#Visualize predictions
plt.figure(figsize=(10,9))
for n in range(30):
  plt.subplot(6,5,n+1)
  plt.imshow(image_batch[n])
  plt.title(labels_batch[n])
  plt.axis('off')
_ = plt.suptitle("Model predictions")

#Accuracy of test set
prediction_indices = []
for arr in result_batch:
    prediction_indices.append(arr.tolist().index(max(arr)))
label_indices = []
for arr in label_batch:
    label_indices.append(arr.tolist().index(max(arr)))
same_count = 0
for i in np.arange(len(prediction_indices)):
    if prediction_indices[i] == label_indices[i]:
        same_count += 1
accuracy = same_count/len(prediction_indices)
print(accuracy)