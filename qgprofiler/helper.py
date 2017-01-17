import os
import re

XML = re.compile("<([/?!]?\w+)|&(#?\w+);|([^<>&'\"=\s]+)|(\s+)|(.)")

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


def xml_scanner(_xml):

    TAG = 1; ENTITY = 2; STRING = 3; WHITESPACE = 4; SEPARATOR = 5

    def gettoken(space=0, scan=XML.scanner(_xml).match):
        try:
            while 1:
                m = scan()
                code = m.lastindex
                text = m.group(code)
                if not space or code != WHITESPACE:
                    return code, text
        except AttributeError:
            raise EOFError

    try:
        while 1:
            code, text = gettoken()
            if code == TAG:
                _type = text[:1]
                if _type == '/':
                    yield 'END', str(text[1:])
                    code, text = gettoken(1)
                    if text != '>':
                        raise SyntaxError, 'not proper end tag'
                else:
                    tag = text
                    attrib = {}
                    while 1:
                        code, text = gettoken(1)
                        if text == '>':
                            yield 'START', str(tag), attrib
                            break
                        if text == '/':
                            yield 'START', str(tag), attrib
                            yield 'END', str(tag)
                            break
                        if text == '?':
                            if _type != text:
                                raise SyntaxError, 'unexpected quotation mark'
                            code, text = gettoken(1)
                            if text != '>':
                                raise SyntaxError, 'expected end tag'
                            break
                        if code == STRING:
                            key = text
                            code, text = gettoken(1)
                            if text != '=':
                                raise SyntaxError, 'expected equal sign'
                            code, quote = gettoken(1)
                            if quote != "'" and quote != '"':
                                raise SyntaxError, 'expected quote'
                            value = []
                            while 1:
                                code, text = gettoken()
                                if text == quote:
                                    break
                                if code == ENTITY:
                                    try:
                                        text = fixentity(text)
                                    except ValueError:
                                        text = text
                                value.append(text)
                            attrib[key] = "".join(value)
    except EOFError:
        pass
    except SyntaxError:
        raise

