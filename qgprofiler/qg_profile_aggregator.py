from node import Node, NodeList
from .qg_profiler import QGProfiler
from .helper import get_real_file_path, get_file_type, xml_scanner, read_attributes_from_xml, merge_attributes
import glob
import json

class QGProfileAggregator(object):
    def __init__(self, in_file_path, out_file_path):
        self.root_node = Node('i_am_root', None, {})
        self.in_file_path = get_real_file_path(in_file_path)
        get_file_type(out_file_path)
        self.out_file_path = get_real_file_path(out_file_path)

    def add_json(self, _json):
        new_node = self.make_node_from_json(_json, self.root_node)
        new_node_list = NodeList()
        new_node_list.append(new_node)
        self.merge_node_list_to_node(self.root_node, new_node_list)

    def merge_node_list_to_node(self, main_node, node_list):
        for node in node_list:
            index = main_node.is_child_in_children(node.get_name())
            if index == -1:
                main_node.add_child(node)
            else:
                existing_node = main_node.get_child(index)
                existing_node.increment_value_by(node.get_value())
                existing_node.increment_count_by(node.get_count())
                existing_node.set_aggregate_attr(merge_attributes(node.get_aggregate_attr(), existing_node.get_aggregate_attr()))
                existing_node.update_over_head(node.get_over_head())
                self.merge_node_list_to_node(existing_node, node.get_children())

    def make_node_from_json(self, _json, parent_node):
        name = _json['name']
        value = _json['value']
        count = _json['count']
        children = _json['children']
        attributes = _json.get('attributes', {})
        over_head = _json.get('overhead', 0)
        new_node = Node(name, parent_node, attributes)
        new_node.set_value(value)
        new_node.set_count(count)
        new_node.set_over_head(over_head)

        for child in children:
            child_node = self.make_node_from_json(child, new_node)
            new_node.add_child(child_node)
        return new_node

    def add_xml(self, _xml):
        current_node = self.root_node
        xml_gen = xml_scanner(_xml)
        for each in xml_gen:
            if each[0] == 'START':
                name = str(each[2]['name'])
                value = float(each[2]['value'])
                count = int(each[2]['count'])
                over_head = float(each[2].get('overhead', 0))
                attributes = read_attributes_from_xml(each[2].get('attributes', {}))
                index = current_node.is_child_in_children(name)
                if index == -1:
                    new_node = Node(name, current_node, attributes)
                    new_node.set_value(value)
                    new_node.set_count(count)
                    new_node.set_over_head(over_head)
                    current_node.add_child(new_node)
                    current_node = new_node
                else:
                    current_node = current_node.get_child(index)
                    current_node.increment_value_by(value)
                    current_node.increment_count_by(count)
                    current_node.set_aggregate_attr(merge_attributes(attributes, current_node.get_aggregate_attr()))
                    current_node.update_over_head(over_head)
            elif each[0] == 'END':
                current_node = current_node.get_parent()

    def generate_file(self, rounding_no=6):
        for file_path in glob.iglob(self.in_file_path):
            filename = file_path.split('/')[-1]
            if filename.endswith('.json'):
                with open(file_path, 'r') as f:
                    raw_json = f.read()
                    _json = json.loads(raw_json)
                    self.add_json(_json)
            elif filename.endswith('.xml'):
                with open(file_path, 'r') as f:
                    _xml = f.read()
                    self.add_xml(_xml)

        qg_profiler = QGProfiler('test', self.out_file_path)
        if len(self.root_node.get_children()) == 1:
            qg_profiler.root_node = self.root_node.get_child(0)
        else:
            qg_profiler.root_node = self.root_node
        qg_profiler.generate_file(rounding_no)
