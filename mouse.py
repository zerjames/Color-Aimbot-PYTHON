import sys
import time
import ctypes

class MouseController:
    def __init__(self):
        # Definir las estructuras y funciones necesarias
        self.user32 = ctypes.WinDLL('user32')
        self.mouse_event = self.user32.mouse_event
        self.MOUSEEVENTF_MOVE = 0x0001
        self.MOUSEEVENTF_ABSOLUTE = 0x8000

    def move(self, x, y):
        # Mueve el mouse en relación a su posición actual
        self.mouse_event(self.MOUSEEVENTF_MOVE, int(x), int(y), 0, 0)
        time.sleep(0.01)

    def click(self):
        # Simula un clic izquierdo
        self.mouse_event(0x0002, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
        self.mouse_event(0x0004, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP

    def flick(self, x, y):
        # Realiza un movimiento rápido de flick
        self.move(x, y)
        time.sleep(0.05)  # Ajusta la pausa según sea necesario para un efecto de "flick"

if __name__ == '__main__':
    mouse = MouseController()
    
    # Ejemplo de uso
    mouse.move(100, 100)  # Mover el mouse 100 píxeles a la derecha y 100 hacia abajo
    mouse.click()         # Hacer clic izquierdo
    mouse.flick(200, 200) # Realizar un flick a la posición 200, 200
