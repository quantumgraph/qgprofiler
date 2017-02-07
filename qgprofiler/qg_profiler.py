import json
from datetime import datetime
from copy import deepcopy
from .node import Node, NodeList
from .helper import get_real_file_path, get_file_type, get_node_attributes, make_attributes_for_xml, merge_attributes
from .constants import HTML1_TXT, HTML2_TXT

class QGProfiler(object):
    def __init__(self, root_name, file_path, attributes={}):
        self.attributes = get_node_attributes(attributes)
        self.root_node = Node(root_name, None, self.attributes)
        self.current_node = self.root_node
        self.file_type = get_file_type(file_path)
        self.file_path = get_real_file_path(file_path)

    def push(self, name):
        datetime_now = datetime.now()
        index = self.current_node.is_child_in_children(name)
        if index == -1:
            new_node = Node(name, self.current_node, self.attributes)
            self.current_node.add_child(new_node)
            self.current_node = new_node
        else:
            self.current_node = self.current_node.get_child(index)
            self.current_node.increment_count()
            self.current_node.modify_time()
        self.current_node.update_over_head((datetime.now() - datetime_now).total_seconds())

    def update(self, attr, value):
        datetime_now = datetime.now()
        if attr in self.attributes:
            self.current_node.update_attribute(attr, value)
            self.current_node.update_over_head((datetime.now() - datetime_now).total_seconds())
        else:
            raise ValueError('cannot update attribute which is not intialized')

    def pop(self):
        datetime_now = datetime.now()
        if self.root_node != self.current_node:
            self.current_node.increment_value()
            self.current_node.modify_time()
            self.current_node.set_aggregate_attr(merge_attributes(self.current_node.get_attributes(), self.current_node.get_aggregate_attr()))
            parent_node = self.current_node.get_parent()
            parent_node.set_attributes(merge_attributes(parent_node.get_attributes(), self.current_node.get_attributes()))
            self.current_node.set_attributes(deepcopy(self.attributes))
            self.current_node.update_over_head((datetime.now() - datetime_now).total_seconds())
            self.current_node = parent_node
        else:
            raise ValueError('cannot pop! you have reached root node, try end')

    def pop_all(self):
        while self.root_node != self.current_node:
            self.pop()

    def end(self):
        datetime_now = datetime.now()
        if self.root_node == self.current_node:
            self.root_node.increment_value()
            self.root_node.modify_time()
            self.root_node.set_aggregate_attr(merge_attributes(self.root_node.get_attributes(), self.root_node.get_aggregate_attr()))
            self.root_node.update_over_head((datetime.now() - datetime_now).total_seconds())
        else:
            raise ValueError('cannot end! you are not at the root node, try pop() or pop_all()')

    def generate_file(self, rounding_no=None):
        def recursive_json_generator(node):
            _dict = {}
            value = node.get_value()
            if rounding_no or rounding_no == 0:
                value = round(value, rounding_no)
            _dict['name'] = node.get_name()
            _dict['value'] = value
            _dict['count'] = node.get_count()
            _dict['overhead'] = node.get_over_head()
            _dict['attributes'] = node.get_aggregate_attr()
            _dict['children'] = [recursive_json_generator(child_node) for child_node in node.get_children()]
            return _dict

        def recursive_xml_generator(node):
            node_name = node.get_name()
            node_value = node.get_value()
            if rounding_no or rounding_no == 0:
                node_value = round(node_value, rounding_no)
            node_value = str(node_value)
            node_count = str(node.get_count())
            node_over_head = str(node.get_over_head())
            node_attributes = make_attributes_for_xml(node.get_aggregate_attr())
            _xml = '<node '+ 'name="' + node_name + '" value="' + node_value + '" count="' + node_count + '" overhead="' + node_over_head + '" attributes="' + node_attributes + '">'
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
