import os

def import_folder(path):
    surface_list = []

    if not os.path.exists(path):
        print(f"[ERROR] Path does not exist: {path}")
        return surface_list

    for folder in os.walk(path):
        print(folder)

    return surface_list
