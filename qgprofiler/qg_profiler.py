import json
from .node import Node, NodeList
from .helper import make_folder

class QGProfiler(object):
    def __init__(self, root_name, folder_path, file_name):
        self.root_node = Node(root_name, None)
        self.current_node = self.root_node
        self.folder_path = make_folder(folder_path)
        self.file_name = file_name

    def push(self, name):
        index = self.current_node.is_child_in_children(name)
        if index == -1:
            new_node = Node(name, self.current_node)
            self.current_node.add_child(new_node)
            self.current_node = new_node
        else:
            self.current_node = self.current_node.get_child(index)
            self.current_node.modify_time()

    def pop(self):
        if self.root_node != self.current_node:
            self.current_node.increment_value()
            self.current_node.modify_time()
            self.current_node = self.current_node.get_parent()
        else:
            raise ValueError('You have reached root node, try end')

    def end(self):
        if self.root_node == self.current_node:
            self.root_node.increment_value()
            self.root_node.modify_time()
        else:
            raise ValueError('You are not at the root node')

    def generate_file(self, _type):
        def recursive_json_generator(node):
            _dict = {}
            _dict['name'] = node.get_name()
            _dict['value'] = node.get_value()
            _dict['children'] = [recursive_json_generator(child_node) for child_node in node.get_children()]
            return json.dumps(_dict)

        def recursive_xml_generator(node):
            _xml = '<' + node.get_name() + ' value="' + str(node.get_value()) + '">'
            _xml += ''.join([recursive_xml_generator(child_node) for child_node in node.get_children()]) 
            _xml += '</' + node.get_name() + '>'
            return _xml

        if _type == 'json':
            text = recursive_json_generator(self.root_node)
            filename = '/'.join([self.folder_path, self.file_name]) + '.json'
        elif _type == 'xml':
            text = recursive_xml_generator(self.root_node)
            filename = '/'.join([self.folder_path, self.file_name]) + '.xml'
        else:
            raise ValueError('Only "json" and "xml" are accepted as an argument')

        with open(filename, 'w') as f:
            f.write(text)
