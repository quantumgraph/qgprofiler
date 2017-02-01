import os
import re

XML = re.compile("<([/?!]?\w+)|&(#?\w+);|([^<>&'\"=\s]+)|(\s+)|(.)")

XML_ENTITIES = {'amp': '&', 'apos': "'", 'gt': '>', 'lt': '<', 'quot': '"'}

def make_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_file_type(file_path):
    filename = file_path.split('/')[-1]
    if filename.endswith('.json'):
        return 'json'
    elif filename.endswith('.xml'):
        return 'xml'
    elif filename.endswith('.html'):
        return 'html'
    else:
        raise ValueError('filename should either end with .json or .xml or .html')

def get_real_file_path(file_path):
    filename = file_path.split('/')[-1]
    folder_path = '/'.join(file_path.split('/')[:-1])
    folder_path = os.path.realpath(os.path.expanduser(folder_path))
    make_folder(folder_path)
    file_path = os.path.join(folder_path, filename)
    return file_path

def get_node_attributes(attributes):
    _dict = {}
    for k, v in attributes.iteritems():
        if v == 'max' or v == 'sum':
            _dict[k] = {'type': v, 'value': 0}
        else:
            raise ValueError('attributes value should be either "max" or "sum"')
    return _dict

def read_attributes_from_xml(attributes_text):
    _dict = {}
    for each_attribute in attributes_text.split(', '):
        _list = each_attribute.split(':')
        _dict[_list[0]] = {'type': _list[1], 'value': float(_list[2])}
    return _dict

def make_attributes_for_xml(_dict):
    _xml = []
    for k, v in _dict.iteritems():
        txt = '{0}:{1}:{2}'.format(k, v['type'], v['value'])
        _xml.append(txt)
    return ', '.join(_xml)

def merge_attributes(attribute_one, attribute_two):
    not_found = []
    for k, v in attribute_one.iteritems():
        if k in attribute_two:
            if v['type'] == 'max':
                if attribute_two[k]['type'] != 'max':
                    raise ValueError('unable to combine same attribute with different type "max" and "sum"')
                attribute_two[k]['value'] = max(v['value'], attribute_two[k]['value'])
            elif v['type'] == 'sum':
                if attribute_two[k]['type'] != 'sum':
                    raise ValueError('unable to combine same attribute with different type "max" and "sum"')
                attribute_two[k]['value'] += v['value']
        else:
            not_found.append(k)
    for k in not_found:
        attribute_two[k] = attribute_one[k]
    return attribute_two

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

def fixentity(entity):
    try:
        return XML_ENTITIES[entity]
    except KeyError:
        pass
    if entity[:2] == '#x':
        value = int(entity[2:], 16)
    else:
        value = int(entity[1:])
    if value > 127:
        return unichr(value)
    return chr(value)
