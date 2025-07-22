import os
import pygame

def import_folder(path):
    surface_list = []

    if not os.path.exists(path):
        print(f"[ERROR] Path does not exist: {path}")
        return surface_list

    for _, _, img_files in os.walk(path):
        for image in img_files:
            full_path = f'{path}/{image}'
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list
