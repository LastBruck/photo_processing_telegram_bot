from rembg import remove
from PIL import Image
from pathlib import Path
from distutils.command.config import config
from PIL import Image
import pytesseract



def remove_bg(id, images_path):
    Path(f'input/{id}/').mkdir(parents=True, exist_ok=True)
    Path(f'output/{id}/').mkdir(parents=True, exist_ok=True)
    input_path = Path(images_path)
    file_name = input_path.stem
    input_img = Image.open(input_path)
    output_img = remove(input_img)
    output_path = f'output/{id}/{file_name}_output.png'
    output_img.save(output_path)
    return output_path



def text_from_img(id, images_path):
    Path(f'input/{id}/').mkdir(parents=True, exist_ok=True)
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    img = Image.open(images_path)
    config = r'--oem 1 --psm 6'
    text = pytesseract.image_to_string(img, lang='rus+eng', config=config)
    return text