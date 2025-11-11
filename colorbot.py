import cv2
import numpy as np
import win32api
import winsound  # Para reproducir sonidos
from capture import Capture
from mouse import MouseController
from settings import Settings

class Colorbot:
    settings = Settings()

    def __init__(self, x, y, xfov, yfov):
        self.settings = Settings()
        self.mouse = MouseController()
        self.grabber = Capture(x, y, xfov, yfov)
        self.LOWER_COLOR, self.UPPER_COLOR = self.get_colors()  # Pastikan bahwa get_colors sudah didefinisikan
        self.aimbot_active_f1 = False  # Status awal aimbot dengan F1 dinonaktifkan.
        self.F1_KEY = 0x70  # Kode tombol untuk F1.
        self.configure()

    def configure(self):
        self.xspeed = lambda: self.settings.get_float('AIMBOT', 'xSpeed')
        self.yspeed = lambda: self.settings.get_float('AIMBOT', 'ySpeed')
        self.AIMBOT_KEY = int(self.settings.get('AIMBOT', 'toggleKey'), 16)  # Tombol aktivasi asli
        self.TARGET_OFFSET = float(self.settings.get('AIMBOT', 'targetOffset'))

    def get_colors(self):
        """Fungsi buat dapetin batas bawah sama batas atas warnanya."""
        lower_color = np.array([0, 120, 70])
        upper_color = np.array([10, 255, 255])
        return lower_color, upper_color

    def toggle_aimbot_f1(self):
        """Fungsi buat nyalain/matiin aimbot pakai tombol F1."""
        self.aimbot_active_f1 = not self.aimbot_active_f1 # Ganti status (nyala/mati) aimbot F1.

        if self.aimbot_active_f1:
            winsound.Beep(1000, 300)  # Bunyi pas dinyalain pakai F1 (frekuensi 1000Hz, durasinya 300 milidetik)
            print("Aimbot-nya nyala otomatis pakai F1.")
        else:
            winsound.Beep(500, 300)  # Bunyi pas dimatiin pakai F1 (frekuensi 500Hz, durasinya 300 milidetik)
            print("Aimbot dinonaktifkan secara otomatis dengan F1")

    def listen(self):
        while True:
            # Kalau F1 dipencet, aimbot otomatisnya di-toggle (diaktifkan/dinonaktifkan)
            if win32api.GetAsyncKeyState(self.F1_KEY) < 0:
                self.toggle_aimbot_f1()

                # Jeda bentar ya, biar tombolnya nggak kedeteksi berkali-kali
                while win32api.GetAsyncKeyState(self.F1_KEY) < 0:
                    pass

            # Jika tombol asli (original key) aimbot sudah ditetapkan dan ditekan
            if win32api.GetAsyncKeyState(self.AIMBOT_KEY) < 0:
                # Proses selama tombol yang ditetapkan ditahan
                self.process()

            # Kalau aimbot F1-nya lagi nyala, langsung jalanin aja prosesnya otomatis
            if self.aimbot_active_f1:
                self.process()

    def process(self):
        hsv = cv2.cvtColor(self.grabber.get_screen(), cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER_COLOR, self.UPPER_COLOR)
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if contours:
            screen_center = (self.grabber.xfov // 2, self.grabber.yfov // 2)
            min_distance = float('inf')
            closest_contour = None

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + w // 2, y + h // 2)
                distance = ((center[0] - screen_center[0]) ** 2 + (center[1] - screen_center[1]) ** 2) ** 0.5

                if distance < min_distance:
                    min_distance = distance
                    closest_contour = contour

            x, y, w, h = cv2.boundingRect(closest_contour)
            center = (x + w // 2, y + h // 2)
            cX = center[0]
            cY = y + int(h * self.TARGET_OFFSET)
            x_diff = cX - self.grabber.xfov // 2
            y_diff = cY - self.grabber.yfov // 2
            self.mouse.move(self.xspeed() * x_diff, self.yspeed() * y_diff)
