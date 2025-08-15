from PIL import Image
import numpy as np

def threshold_transparency(image_path, output_path, threshold=255):
    img = Image.open(image_path).convert('RGBA')
    
    data = np.array(img)
    
    data[:, :, 3] = np.where(data[:, :, 3] >= threshold, 255, 0)
    
    result = Image.fromarray(data, 'RGBA')
    result.save(output_path)

threshold_transparency('nazrin.png', 'nazrin_new.png', threshold=150)