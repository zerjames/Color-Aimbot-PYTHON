import pyautogui
import ctypes
import os
import shutil
from colorbot import Colorbot
from settings import Settings
import configparser

# Kode ANSI untuk warna
GREEN_NEON = "\033[92m"  # Hijau terang
PURPLE = "\033[95m"      # Ungu
RESET = "\033[0m"        # Mengembalikan warna ke default

class Main:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        self.settings = Settings()
        self.monitor = pyautogui.size()
        self.CENTER_X, self.CENTER_Y = self.monitor.width // 2, self.monitor.height // 2
        self.XFOV = self.settings.get_int('AIMBOT', 'xFov')
        self.YFOV = self.settings.get_int('AIMBOT', 'yFov')
        self.Colorbot = Colorbot(self.CENTER_X - self.XFOV // 2, self.CENTER_Y - self.YFOV // 2, self.XFOV, self.YFOV)

    def better_cmd(self, width, height):
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
            style &= -262145
            style &= -65537
            ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
        STD_OUTPUT_HANDLE_ID = ctypes.c_ulong(4294967285)
        windll = ctypes.windll.kernel32
        handle = windll.GetStdHandle(STD_OUTPUT_HANDLE_ID)
        rect = ctypes.wintypes.SMALL_RECT(0, 0, width - 1, height - 1)
        windll.SetConsoleScreenBufferSize(handle, ctypes.wintypes._COORD(width, height))
        windll.SetConsoleWindowInfo(handle, ctypes.c_int(True), ctypes.pointer(rect))

    def get_console_width(self):
        """Mengambil lebar konsol."""
        size = shutil.get_terminal_size((80, 20))  # (lebar default, tinggi)
        return size.columns

    def center_text(self, text):
        """Memusatkan teks di konsol."""
        console_width = self.get_console_width()
        for line in text.splitlines():
            print(line.center(console_width))

    def configure_sensitivity(self):
        """Menampilkan sensitivitas dan memungkinkan pengguna mengubahnya."""
        x_speed = self.config.getfloat('AIMBOT', 'xSpeed')
        y_speed = self.config.getfloat('AIMBOT', 'ySpeed')

        # Menampilkan sensitivitas saat ini.
        print(f"{PURPLE}Place enemy in game color: Purple.{RESET}")  # Mensaje en púrpura
        print()
        print(f'Current sensitivity: {x_speed} (X)')
        change = input(f'{GREEN_NEON}Do you want to change the sensitivity? (S/N): {RESET}').strip().lower()

        if change == 's':
            # Meminta nilai sensitivitas baru dalam satu baris
            new_sensitivity = input(f'New sensitivity (Current: {x_speed} (X), {y_speed} (Y)): ').strip()

            if new_sensitivity:
                # Memisahkan nilai-nilai baru yang dimasukkan oleh pengguna.
                try:
                    new_x_speed, new_y_speed = map(float, new_sensitivity.split(','))
                    self.config.set('AIMBOT', 'xSpeed', str(new_x_speed))
                    self.config.set('AIMBOT', 'ySpeed', str(new_y_speed))
                    
                    # Menyimpan perubahan ke dalam file settings.ini
                    with open('settings.ini', 'w') as configfile:
                        self.config.write(configfile)

                    print(f'Updated sensitivity: {new_x_speed} (X)')
                except ValueError:
                    print("Error: Please enter the values ​​in the correct format (example: 2.0, 1.5).")
        else:
            print("Cheat sedang berjalan...")  # Pesan ketika sensitivitas tidak diubah.

    def configure_toggle_key(self):
        """Mostrar la tecla togglekey y permitir al usuario cambiarla."""
        current_toggle_key = self.config.get('AIMBOT', 'togglekey')
        print(f'Current key for togglekey: {current_toggle_key}')
        change = input(f'{GREEN_NEON}Do you want to change the togglekey? (Y/N): {RESET}').strip().lower()

        if change == 's':
            new_toggle_key = input('Enter the new value for togglekey (example: 0x02): ').strip()
            self.config.set('AIMBOT', 'togglekey', new_toggle_key)

            # Guardar los cambios en el archivo settings.ini
            with open('settings.ini', 'w') as configfile:
                self.config.write(configfile)

            print(f'Toggle key updated to: {new_toggle_key}')
        else:
            print("Cheat running...")  # Mensaje al no cambiar la tecla

    def info(self):
        os.system('cls')  # Membersihkan konsol.
        ascii_art = """
███████╗███████╗██████╗      ██╗     ██╗ █████╗ ███╗   ███╗███████╗███████╗
╚══███╔╝██╔════╝██╔══██╗     ██║     ██║██╔══██╗████╗ ████║██╔════╝██╔════╝
  ███╔╝ █████╗  ██████╔╝     ██║     ██║███████║██╔████╔██║█████╗  █████╗  
 ███╔╝  ██╔══╝  ██╔══██╗     ██║     ██║██╔══██║██║╚██╔╝██║██╔══╝  ██╔══╝  
███████╗███████╗██║  ██║     ███████╗██║██║  ██║██║ ╚═╝ ██║███████╗███████╗
╚══════╝╚══════╝╚═╝  ╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝
  
        """
        self.center_text(ascii_art)  # Memusatkan seni ASCII
        self.configure_sensitivity()  # Mengatur sensitivitas

    def run(self):
        self.better_cmd(120, 30)
        self.configure_toggle_key()  # Konfigurasikan tombol togglekey sebelum menjalankan program
        self.info()
        self.Colorbot.listen()

if __name__ == '__main__':
    Main().run()
