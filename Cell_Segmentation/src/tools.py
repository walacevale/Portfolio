import os
import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import keras.backend as K
import tensorflow as tf


def normalized_image(img):
  mean = np.mean(img)
  std = np.std(img)
  normalized_img = (img - mean) / (std + 1e-7)
  return normalized_img


def load_data(image_dir, mask_dir, img_size=(512, 512)):
    images = []
    masks = []
    
    image_files = sorted([f for f in os.listdir(image_dir) if f.endswith(('.bmp', '.tif', '.png'))])
    mask_files  = sorted([f for f in os.listdir(mask_dir)  if f.endswith(('.png', '.tif'))])   
    for img_file, mask_file in zip(image_files, mask_files):
        
        img_path = os.path.join(image_dir, img_file)
        img = load_img(img_path, target_size=img_size, color_mode='grayscale')
        img = normalized_image(img_to_array(img))
        images.append(img)
        
        mask_path = os.path.join(mask_dir, mask_file)
        mask = load_img(mask_path, target_size=img_size, color_mode='grayscale')
        mask = img_to_array(mask)
        mask = np.where(mask > 0.5, 1, 0.0)
        masks.append(mask)
    
    images = np.array(images)
    masks = np.array(masks)
    
    return images, masks


def dice_loss(y_true, y_pred, smooth=1e-6):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    intersection = tf.reduce_sum(y_true * y_pred)
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred)

    dice = (2. * intersection + smooth) / (union + smooth)

    return 1.0 - dice

def dice_coefficient(y_true, y_pred, smooth=1e-6):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    intersection = tf.reduce_sum(y_true * y_pred)
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred)

    dice = (2. * intersection + smooth) / (union + smooth)

    return dice


