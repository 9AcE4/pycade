#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import ctypes
from ctypes import wintypes

import pygame
#-----------------------------

#=============================#
# CONSTANTS                   #
#=============================#
#-----------------------------
LOGICAL_WIDTH = 640
LOGICAL_HEIGHT = 360

DEFAULT_SCALE = 1

SWP_NOSIZE = 0x0001
SWP_NOZORDER = 0x0004
#-----------------------------

#=============================#
# FUNCTIONS                   #
#=============================#
#-----------------------------
def create_window(scale=DEFAULT_SCALE):
    width = LOGICAL_WIDTH * scale
    height = LOGICAL_HEIGHT * scale

    window = pygame.display.set_mode(
        (width, height),
        pygame.NOFRAME
    )

    pygame.display.set_caption("PyCade")

    logical_surface = pygame.Surface(
        (LOGICAL_WIDTH, LOGICAL_HEIGHT)
    )

    return window, logical_surface
#-----------------------------
def get_window_handle():
    window_info = pygame.display.get_wm_info()

    return window_info["window"]
#-----------------------------
def get_window_position():
    hwnd = get_window_handle()

    rect = wintypes.RECT()

    ctypes.windll.user32.GetWindowRect(
        hwnd,
        ctypes.byref(rect)
    )

    return rect.left, rect.top
#-----------------------------
def get_cursor_position():
    point = wintypes.POINT()

    ctypes.windll.user32.GetCursorPos(
        ctypes.byref(point)
    )

    return point.x, point.y
#-----------------------------
def move_window(x, y):
    hwnd = get_window_handle()

    ctypes.windll.user32.SetWindowPos(
        hwnd,
        None,
        x,
        y,
        0,
        0,
        SWP_NOSIZE | SWP_NOZORDER
    )
#-----------------------------