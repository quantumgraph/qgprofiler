import os

def make_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def make_folder_and_get_file_type(file_path):
    filename = file_path.split('/')[-1]
    if filename.endswith('.json'):
        file_type = 'json'
    elif filename.endswith('.xml'):
        file_type = 'xml'
    else:
        raise ValueError('filename should either end with .json or .xml')
    folder_path = '/'.join(file_path.split('/')[:-1])
    make_folder(folder_path)
    return file_type

