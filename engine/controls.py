#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
import pygame
#-----------------------------


#=============================#
# FUNCTIONS                   #
#=============================#
#-----------------------------
def handle_global_events(events):
    for event in events:
        if event.type == pygame.QUIT:
            return False

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


#=============================#
# MENU CONFIRM                #
#=============================#
#-----------------------------
def get_menu_confirm(events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER
            ):
                return True

    return False
#-----------------------------


#=============================#
# MENU BACK                   #
#=============================#
#-----------------------------
def get_menu_back(events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True

    return False
#-----------------------------