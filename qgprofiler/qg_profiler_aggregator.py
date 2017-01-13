from node import Node, NodeList
from .qg_profiler import QGProfiler
from .helper import make_folder

class QGProfileAggregator(object):
    def __init__(self, folder_path, file_name):
        self.root_node = Node('i_am_root', None)
        self.folder_path = make_folder(folder_path)
        self.file_name = file_name

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
                existing_node.set_value(node.get_value() + existing_node.get_value())
                self.merge_node_list_to_node(existing_node, node.get_children())

    def make_node_from_json(self, _json, parent_node):
        name = _json['name']
        value = _json['value']
        children = _json['children']
        new_node = Node(name, parent_node)
        new_node.set_value(value)

        for child in children:
            child_node = self.make_node_from_json(child, new_node)
            new_node.add_child(child_node)
        return new_node

    def generate_file(self, _type):
        qg_profiler = QGProfiler('test', self.folder_path, self.file_name)
        qg_profiler.root_node = self.root_node
        return qg_profiler.generate_file(_type)
