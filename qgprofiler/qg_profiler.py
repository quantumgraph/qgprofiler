from .node import Node, NodeList
from .helper import get_real_file_path, get_file_type, get_node_attributes, make_attributes_for_xml, merge_attributes
import json
from .constants import HTML1_TXT, HTML2_TXT

class QGProfiler(object):
    def __init__(self, root_name, file_path, attributes={}):
        self.attributes = get_node_attributes(attributes)
        self.root_node = Node(root_name, None, self.attributes)
        self.current_node = self.root_node
        self.file_type = get_file_type(file_path)
        self.file_path = get_real_file_path(file_path)

    def push(self, name):
        index = self.current_node.is_child_in_children(name)
        if index == -1:
            new_node = Node(name, self.current_node, self.attributes)
            self.current_node.add_child(new_node)
            self.current_node = new_node
        else:
            self.current_node = self.current_node.get_child(index)
            self.current_node.increment_count()
            self.current_node.modify_time()

    def update(self, attr, value):
        if attr in self.attributes:
            self.current_node.update_attribute(attr, value)
        else:
            raise ValueError('cannot update attribute which is not intialized')

    def pop(self):
        if self.root_node != self.current_node:
            self.current_node.increment_value()
            self.current_node.modify_time()
            self.current_node = self.current_node.get_parent()
        else:
            raise ValueError('cannot pop! you have reached root node, try end')

    def pop_all(self):
        while self.root_node != self.current_node:
            self.pop()

    def end(self):
        if self.root_node == self.current_node:
            self.root_node.increment_value()
            self.root_node.modify_time()
        else:
            raise ValueError('cannot end! you are not at the root node, try pop() or pop_all()')

    def __float_attributes_to_parent(self, node):
        if len(node.get_children()) == 0:
            if node != self.root_node:
                parent_node = node.get_parent()
                parent_node.set_attributes(merge_attributes(parent_node.get_attributes(), node.get_attributes()))
        else:
            for child_node in node.get_children():
                self.__float_attributes_to_parent(child_node)
        return node

    def generate_file(self, rounding_no=None):
        def recursive_json_generator(node):
            _dict = {}
            value = node.get_value()
            if rounding_no or rounding_no == 0:
                value = round(value, rounding_no)
            _dict['name'] = node.get_name()
            _dict['value'] = value
            _dict['count'] = node.get_count()
            _dict['attributes'] = node.get_attributes()
            _dict['children'] = [recursive_json_generator(child_node) for child_node in node.get_children()]
            return _dict

        def recursive_xml_generator(node):
            node_name = node.get_name()
            node_value = node.get_value()
            if rounding_no or rounding_no == 0:
                node_value = round(node_value, rounding_no)
            node_value = str(node_value)
            node_count = str(node.get_count())
            node_attributes = make_attributes_for_xml(node.get_attributes())
            _xml = '<node '+ 'name="' + node_name + '" value="' + node_value + '" count="' + node_count + '" attributes="' + node_attributes + '">'
            _xml += ''.join([recursive_xml_generator(child_node) for child_node in node.get_children()]) 
            _xml += '</node>'
            return _xml

        if self.file_type == 'json':
            _json = recursive_json_generator(self.root_node)
            text = json.dumps(_json)
            self.write_file(text)
        elif self.file_type == 'xml':
            text = recursive_xml_generator(self.root_node)
            self.write_file(text)
        elif self.file_type == 'html':
            _json = recursive_json_generator(self.root_node)
            text = json.dumps(_json)
            html_text = HTML1_TXT + text + HTML2_TXT
            self.write_file(html_text)

    def write_file(self, text):
        with open(self.file_path, 'w') as f:
            f.write(text)
