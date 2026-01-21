import cv2
import numpy as np
import os
from skimage import measure
from skimage.measure import label, regionprops

path_folder_train = r'C:\Users\walla\Downloads\ML-Final\Create_model\Dataset\Original-images\train - Original'
path_folder_masks = r'C:\Users\walla\Downloads\ML-Final\Create_model\Dataset\Original-images\mask - Original

save_path_images = r'C:\Users\walla\Downloads\ML-Final\Create_model\Dataset/images'
save_path_masks = r'C:\Users\walla\Downloads\ML-Final\Create_model\Dataset/masks'


os.makedirs(save_path_images, exist_ok=True)
os.makedirs(save_path_masks, exist_ok=True)


def crop_patch_around_centroid(image, masks, centroid, patch_size=128):
    h, w = np.shape(image)
    cy, cx = int(centroid[0]), int(centroid[1])
    half = patch_size // 2

    # Coordenadas do retângulo
    y1 = max(cy - half, 0)
    y2 = min(cy + half, h)
    x1 = max(cx - half, 0)
    x2 = min(cx + half, w)

    # Ajusta tamanho se for menor nas bordas
    patch_image = np.zeros((patch_size, patch_size), dtype=image.dtype)
    patch_masks = np.zeros((patch_size, patch_size), dtype=image.dtype)

    cropped_image = image[y1:y2, x1:x2]
    cropped_masks = masks[y1:y2, x1:x2]

    patch_image[:y2-y1, :x2-x1] = cropped_image
    patch_masks[:y2-y1, :x2-x1] = cropped_masks

    return patch_image, patch_masks



path_trains =  sorted([
    os.path.join(path_folder_train, f)
    for f in os.listdir(path_folder_train)
    if f.lower().endswith(('.bmp', '.png', '.tif'))
])

path_masks =  sorted([
    os.path.join(path_folder_masks, f)
    for f in os.listdir(path_folder_masks)
    if f.lower().endswith(('.bmp', '.png', '.tif'))
])

# Para cada imagem/máscara
count=0
for path_train, path_mask in zip(path_trains, path_masks):
    # Lê imagem e máscara
    image = cv2.imread(path_train, cv2.IMREAD_GRAYSCALE)
    mask  = cv2.imread(path_mask, cv2.IMREAD_GRAYSCALE)
    mask = np.where(mask > 0.5, 1, 0).astype(np.uint8)    

    # Gera labels e propriedades
    label_image = label(mask, connectivity=1)
    props = regionprops(label_image)

    base_name = os.path.splitext(os.path.basename(path_train))[0]

    for i, region in enumerate(props):

        centroid = region.centroid
        patch_img, patch_mask = crop_patch_around_centroid(image, mask, centroid)

        # Nomes dos arquivos
        img_name =  f"{base_name}_cell{i}.png"
        mask_name = f"{base_name}_cell{i}.png"

        # Salvamento
        cv2.imwrite(os.path.join(save_path_images, img_name), patch_img)
        cv2.imwrite(os.path.join(save_path_masks, img_name), patch_mask)