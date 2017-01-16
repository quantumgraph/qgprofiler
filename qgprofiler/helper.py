import os

def make_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_file_type(file_path):
    filename = file_path.split('/')[-1]
    if filename.endswith('.json'):
        return 'json'
    elif filename.endswith('.xml'):
        return 'xml'
    else:
        raise ValueError('filename should either end with .json or .xml')

def get_real_file_path(file_path):
    filename = file_path.split('/')[-1]
    folder_path = '/'.join(file_path.split('/')[:-1])
    folder_path = os.path.realpath(os.path.expanduser(folder_path))
    make_folder(folder_path)
    file_path = os.path.join(folder_path, filename)
    return file_path

