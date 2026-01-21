import tensorflow as tf
from tensorflow.keras import layers, Model

def unet_reduzida(input_shape=(256, 352, 1)):
    inputs = layers.Input(input_shape)

    # ---------- Encoder ----------
    c1 = layers.Conv2D(32, 3, padding='same', kernel_initializer='he_normal')(inputs)
    c1 = layers.LeakyReLU(0.01)(c1)
    c1 = layers.Conv2D(32, 3, padding='same', kernel_initializer='he_normal')(c1)
    c1 = layers.LeakyReLU(0.01)(c1)
    p1 = layers.MaxPooling2D(2)(c1)

    c2 = layers.Conv2D(64, 3, padding='same', kernel_initializer='he_normal')(p1)
    c2 = layers.LeakyReLU(0.01)(c2)
    c2 = layers.Conv2D(64, 3, padding='same', kernel_initializer='he_normal')(c2)
    c2 = layers.LeakyReLU(0.01)(c2)
    p2 = layers.MaxPooling2D(2)(c2)

    c3 = layers.Conv2D(128, 3, padding='same', kernel_initializer='he_normal')(p2)
    c3 = layers.LeakyReLU(0.01)(c3)
    c3 = layers.Conv2D(128, 3, padding='same', kernel_initializer='he_normal')(c3)
    c3 = layers.LeakyReLU(0.01)(c3)
    p3 = layers.MaxPooling2D(2)(c3)

    c4 = layers.Conv2D(256, 3, padding='same', kernel_initializer='he_normal')(p3)
    c4 = layers.LeakyReLU(0.01)(c4)
    c4 = layers.Conv2D(256, 3, padding='same', kernel_initializer='he_normal')(c4)
    c4 = layers.LeakyReLU(0.01)(c4)
    p4 = layers.MaxPooling2D(2)(c4)

    c5 = layers.Conv2D(512, 3, padding='same', kernel_initializer='he_normal')(p4)
    c5 = layers.LeakyReLU(0.01)(c5)
    c5 = layers.Conv2D(512, 3, padding='same', kernel_initializer='he_normal')(c5)
    c5 = layers.LeakyReLU(0.01)(c5)
    c5 = layers.Dropout(0.2)(c5)

    # ---------- Decoder ----------
    u6 = layers.Conv2DTranspose(256, 2, strides=2, padding='same')(c5)
    u6 = layers.Concatenate()([u6, c4])
    c6 = layers.Conv2D(256, 3, padding='same', kernel_initializer='he_normal')(u6)
    c6 = layers.LeakyReLU(0.01)(c6)
    c6 = layers.Conv2D(256, 3, padding='same', kernel_initializer='he_normal')(c6)
    c6 = layers.LeakyReLU(0.01)(c6)

    u7 = layers.Conv2DTranspose(128, 2, strides=2, padding='same')(c6)
    u7 = layers.Concatenate()([u7, c3])
    c7 = layers.Conv2D(128, 3, padding='same', kernel_initializer='he_normal')(u7)
    c7 = layers.LeakyReLU(0.01)(c7)
    c7 = layers.Conv2D(128, 3, padding='same', kernel_initializer='he_normal')(c7)
    c7 = layers.LeakyReLU(0.01)(c7)

    u8 = layers.Conv2DTranspose(64, 2, strides=2, padding='same')(c7)
    u8 = layers.Concatenate()([u8, c2])
    c8 = layers.Conv2D(64, 3, padding='same', kernel_initializer='he_normal')(u8)
    c8 = layers.LeakyReLU(0.01)(c8)
    c8 = layers.Conv2D(64, 3, padding='same', kernel_initializer='he_normal')(c8)
    c8 = layers.LeakyReLU(0.01)(c8)

    u9 = layers.Conv2DTranspose(32, 2, strides=2, padding='same')(c8)
    u9 = layers.Concatenate()([u9, c1])
    c9 = layers.Conv2D(32, 3, padding='same', kernel_initializer='he_normal')(u9)
    c9 = layers.LeakyReLU(0.01)(c9)
    c9 = layers.Conv2D(32, 3, padding='same', kernel_initializer='he_normal')(c9)
    c9 = layers.LeakyReLU(0.01)(c9)

    outputs = layers.Conv2D(1, 1, activation='sigmoid')(c9)

    return Model(inputs, outputs)
