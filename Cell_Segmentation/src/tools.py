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
    
    # Listar todos os arquivos de imagem nas pastas
    image_files = sorted([f for f in os.listdir(image_dir) if f.endswith(('.bmp', '.tif', '.png'))])
    mask_files  = sorted([f for f in os.listdir(mask_dir)  if f.endswith(('.png', '.tif'))])   
    for img_file, mask_file in zip(image_files, mask_files):
        # Carregar a imagem
        img_path = os.path.join(image_dir, img_file)
        img = load_img(img_path, target_size=img_size, color_mode='grayscale')
        img = normalized_image(img_to_array(img))
        images.append(img)
        
        # Carregar a máscara
        mask_path = os.path.join(mask_dir, mask_file)
        mask = load_img(mask_path, target_size=img_size, color_mode='grayscale')
        mask = img_to_array(mask)
        mask = np.where(mask > 0.5, 1, 0.0)
        masks.append(mask)
    
    # Converter listas para arrays NumPy
    images = np.array(images)
    masks = np.array(masks)
    
    return images, masks


def dice_loss(y_true, y_pred, smooth=1):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)  # Garante que ambos sejam float32
    y_pred = tf.clip_by_value(y_pred, 1e-7, 1 - 1e-7)  # Evita valores extremos
    
    intersection = tf.reduce_sum(y_true * y_pred)
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred)
    dice = (2. * intersection + smooth) / (union + smooth)
    
    return 1 - dice

def dice_coefficient(y_true, y_pred, smooth=1e-6):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    y_pred = tf.clip_by_value(y_pred, 1e-7, 1 - 1e-7)
    intersection = tf.reduce_sum(y_true * y_pred)
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred)
    dice = (2. * intersection + smooth) / (union + smooth)
    return dice

def tversky_loss(y_true, y_pred, alpha=0.9, beta=0.1, smooth=1e-6):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    tp = tf.reduce_sum(y_true * y_pred)
    fp = tf.reduce_sum((1 - y_true) * y_pred)
    fn = tf.reduce_sum(y_true * (1 - y_pred))

    tversky = (tp + smooth) / (tp + alpha*fp + beta*fn + smooth)
    return 1 - tversky


def combined_loss(y_true, y_pred):
    return (
        0.7 * tversky_loss(y_true, y_pred, alpha=0.9, beta=0.1) +
        0.3 * tf.keras.losses.binary_crossentropy(y_true, y_pred)
    )


def focal_tversky_loss(y_true, y_pred, alpha=0.9, beta=0.1, gamma=3, smooth=1e-6):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    axes = (1, 2, 3)

    tp = tf.reduce_sum(y_true * y_pred, axis=axes)
    fp = tf.reduce_sum((1 - y_true) * y_pred, axis=axes)
    fn = tf.reduce_sum(y_true * (1 - y_pred), axis=axes)

    tversky = (tp + smooth) / (tp + alpha * fp + beta * fn + smooth)
    return tf.reduce_mean(tf.pow(1 - tversky, gamma))


import tensorflow as tf

def binary_focal_loss(y_true, y_pred, alpha=0.98, gamma=6.0):
    y_pred = tf.clip_by_value(y_pred, tf.keras.backend.epsilon(), 1. - tf.keras.backend.epsilon())
    bce = - (y_true * tf.math.log(y_pred) + (1 - y_true) * tf.math.log(1 - y_pred))
    loss = alpha * tf.pow(1 - y_pred, gamma) * bce
    return tf.reduce_mean(loss)


from tensorflow.keras.losses import Loss

class SparseCategoricalFocalLoss(Loss):
    def __init__(self, gamma=2., class_weight=None, from_logits=False, name="sparse_categorical_focal_loss"):
        super().__init__(name=name)
        self.gamma = gamma
        self.class_weight = class_weight
        self.from_logits = from_logits

    def call(self, y_true, y_pred):
        # y_true: [batch, h, w] inteiros
        # y_pred: [batch, h, w, n_classes] (softmax)
        y_true = tf.cast(y_true, tf.int32)
        y_true_onehot = tf.one_hot(y_true, depth=tf.shape(y_pred)[-1])
        
        if self.class_weight is not None:
            weights = tf.reduce_sum(y_true_onehot * tf.constant(self.class_weight, dtype=tf.float32), axis=-1)
        else:
            weights = 1.0
        
        if self.from_logits:
            y_pred = tf.nn.softmax(y_pred, axis=-1)
        
        ce = -y_true_onehot * tf.math.log(tf.clip_by_value(y_pred, 1e-7, 1.0))
        loss = tf.reduce_sum(ce, axis=-1)
        loss = weights * loss
        loss = tf.reduce_mean(loss)
        return loss

def bce_dice_loss(y_true, y_pred):
    bce = tf.keras.losses.binary_crossentropy(y_true, y_pred)
    dice = dice_loss(y_true, y_pred)
    return 0.7 * bce + 0.3 * dice
