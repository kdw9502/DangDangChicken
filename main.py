import time
from PIL import Image
from pystray import Menu, MenuItem, Icon
import requests
import threading
import ctypes
import os, sys
import subprocess

bgm = True

class Crawler:
    def __init__(self):
        self.noticed = False


    def run(self):
        while True:
            if self.crawl_homeplus():
                time.sleep(1)
                if self.crawl_homeplus():
                    self.notice("https://front.homeplus.co.kr/item?itemNo=069150196&storeType=HYPER")
            elif self.crawl_auction():
                time.sleep(1)
                if self.crawl_auction():
                    self.notice("http://itempage3.auction.co.kr/DetailView.aspx?itemno=C652681498")
            elif self.crawl_gmarket():
                time.sleep(1)
                if self.crawl_gmarket():
                    self.notice("http://item.gmarket.co.kr/Item?goodscode=2493520744")
            else:
                self.noticed = False
            time.sleep(20)

    def notice(self, url):
        if not self.noticed:
            self.noticed = True
            threading.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, "당당 치킨이 재입고되었습니다.", "당당치킨", 0), daemon=True).start()
            os.system(f"start \"\" \"{url}\"")
            try:
                if bgm:
                    os.system(f"start \"\" \"{resource_path('homeplus.mp3')}\"")
            except Exception as e:
                print(e)

    def crawl_homeplus(self):
        max_try = 5
        for _ in range(max_try):
            response = requests.get("https://front.homeplus.co.kr/item/getItemDetail.json?itemNo=069150196&storeType=HYPER", verify=False)
            json = response.json()
            try:
                return json["data"]["item"]["sale"]["stockQty"] > 0
            except KeyError:
                time.sleep(1)
        return False

    def crawl_auction(self):
        max_try = 5
        for _ in range(max_try):
            response = requests.get("http://itempage3.auction.co.kr/DetailView.aspx?itemno=C652681498", verify=False)
            text = response.text
            if response.ok:
                return "현재 구매가 불가능한 상품입니다." not in text and "품절" not in text
            else:
                time.sleep(1)
        return False

    def crawl_gmarket(self):
        max_try = 5
        for _ in range(max_try):
            response = requests.get("http://item.gmarket.co.kr/Item?goodscode=2493520744", verify=False)
            text = response.text
            if response.ok:
                return "일시품절" not in text and "품절" not in text
            else:
                time.sleep(1)
        return False


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def on_toggle_bgm(icon, item):
    global bgm, sound_process
    bgm = not item.checked

if __name__ == '__main__':
    image = Image.open(resource_path("homeplus.ico"))
    exit_menu = MenuItem('종료', lambda: icon.stop())
    bgm_menu = MenuItem('홈플러스 BGM 재생', on_toggle_bgm, checked=lambda _: bgm)
    menu = Menu(bgm_menu, exit_menu)
    icon = Icon("당당치킨", image, menu=menu)
    crawler = Crawler()
    thread = threading.Thread(target=Crawler.run, args=(crawler,), daemon=True).start()
    icon.run()
