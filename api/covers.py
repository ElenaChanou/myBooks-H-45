import os
import urllib.request
from PIL import Image

def download_cover(url: str, volume_id: str) -> str:
    # dhmiourgei enan local folder ean den uparxei
    folder = "assets/covers"
    os.makedirs(folder, exist_ok=True)

    #ean to cover den uparxei stin Api epistrefei ena default.jpg
    if url is None:
        return "assets/covers/default.jpg"

    #kanei download tin eikona kai save
    path = f"{folder}/{volume_id}.jpg"
    urllib.request.urlretrieve(url, path)

    #kanei thn eikona sto megethos 128x192
    img = Image.open(path)
    # Pillow >= 9.1 uses Image.Resampling.LANCZOS; older versions have Image.LANCZOS
    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.LANCZOS
    img = img.resize((128, 192), resample=resample_filter)
    img.save(path)

    return path

