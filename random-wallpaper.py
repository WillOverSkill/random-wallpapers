import ctypes
import requests
import urllib.request
import win32.lib.win32con as win32con
from configparser import ConfigParser

def getWallpaper() -> str:
    '''Get the save location of the current desktop wallpaper.'''
    output = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER, len(output), output, 0)
    return output.value

def setWallpaper(path: str):
    '''Set desktop wallpaper to be an image defined by path.'''
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, path, win32con.SPIF_UPDATEINIFILE)

def getImageURL(id: str) -> str:
    '''Queries Unsplash API with input id for a random wallpaper image and returns its URL.'''
    query = {
        "query": "wallpaper",
        "orientation": "landscape",
        "client_id": id
    }
    response = requests.get("https://api.unsplash.com/photos/random", params=query)
    response = response.json()

    return response["urls"]["raw"] + "&fit=crop&crop=entropy&fm=jpg&q=85&w=2560&h=1440"

def saveImage(url: str, savePath: str):
    '''Downloads image from url and saves in savePath.'''
    urllib.request.urlretrieve(url, savePath)

def main():
    config = ConfigParser()
    config.read("config.ini")

    savePath = config["CONFIG"]["saveLocation"]
    id = config["CONFIG"]["id"]

    imageURL = getImageURL(id)
    saveImage(imageURL, savePath)
    setWallpaper(savePath)

if __name__ == "__main__":
    main()