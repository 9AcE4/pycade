#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame

from engine.window import get_cursor_position
from engine.window import get_window_position
from engine.window import move_window
#-----------------------------


#=============================#
# VARIABLES                   #
#=============================#
#-----------------------------
dragging = False

drag_mouse_start = (0, 0)
drag_window_start = (0, 0)
#-----------------------------


#=============================#
# FUNCTIONS                   #
#=============================#
#-----------------------------
def handle_global_events(events):
    global dragging
    global drag_mouse_start
    global drag_window_start

    for event in events:
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True

                drag_mouse_start = get_cursor_position()
                drag_window_start = get_window_position()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = get_cursor_position()

                offset_x = (
                    mouse_x
                    - drag_mouse_start[0]
                )

                offset_y = (
                    mouse_y
                    - drag_mouse_start[1]
                )

                new_x = (
                    drag_window_start[0]
                    + offset_x
                )

                new_y = (
                    drag_window_start[1]
                    + offset_y
                )

                move_window(
                    new_x,
                    new_y
                )

    return True
#-----------------------------


#=============================#
# MENU NAVIGATION             #
#=============================#
#-----------------------------
def get_menu_navigation(events):
    navigation = 0

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                navigation -= 1
            elif event.key == pygame.K_DOWN:
                navigation += 1

    return navigation
#-----------------------------
