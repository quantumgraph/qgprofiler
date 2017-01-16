import os

def make_folder(folder_path):
    if folder_path[-1] == '/':
        folder_path = folder_path[:-1]
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def get_folder(folder_path):
    if folder_path[-1] == '/':
        folder_path = folder_path[:-1]
    return folder_path
