import time
from PIL import Image
from pystray import Menu, MenuItem, Icon
import requests
from playsound import playsound
import threading


def main():
    noticed = False
    retry_count = 0
    while True:
        response = requests.get("https://front.homeplus.co.kr/item/getItemDetail.json?itemNo=069150196&storeType=HYPER", verify=False)
        json = response.json()
        is_remain = False
        try:
            is_remain = json["data"]["item"]["sale"]["stockQty"] > 0
            retry_count = 0
        except KeyError:
            retry_count += 1
            if retry_count > 5:
                return
        if is_remain:
            if not noticed:
                noticed = True
                playsound("homeplus.mp3")
        else:
            noticed = False
        time.sleep(20)


if __name__ == '__main__':
    image = Image.open("homeplus.ico")
    menu = Menu(MenuItem('종료', lambda: icon.stop()))
    icon = Icon("당당치킨", image, menu=menu)
    thread = threading.Thread(target=main, daemon=True).start()
    icon.run()
