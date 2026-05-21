import os
import urllib.request

def download_cover(url: str, volume_id: str) -> str:
    # dhmiourgei enan local folder ean den uparxei
    folder = "assets/covers"
    os.makedirs(folder, exist_ok=True)

    #kanei download tin eikona kai save
    path = f"{folder}/{volume_id}.jpg"
    urllib.request.urlretrieve(url, path)

    return path

