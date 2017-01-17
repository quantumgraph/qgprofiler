from datetime import datetime
from copy import deepcopy

class Node(object):
    def __init__(self, name, parent_node):
        self.__name = name
        self.__modified_time = datetime.utcnow()
        self.__parent_node = parent_node
        self.__children_node = NodeList()
        self.__index_of_child = {}
        self.__value = 0
        self.__count = 1

    def __repr__(self):
        return '<%s.Node object with value %s at %s>' %(self.__name, self.__value, hex(id(self)))

    def get_name(self):
        return self.__name

    def get_value(self):
        return self.__value

    def get_count(self):
        return self.__count

    def get_parent(self):
        return self.__parent_node

    def set_value(self, value):
        self.__value = value

    def set_count(self, count):
        self.__count = count

    def increment_value(self):
        datetime_now = datetime.utcnow()
        time_delta = (datetime_now - self.__modified_time).total_seconds()
        self.__value += time_delta

    def increment_value_by(self, value):
        self.__value += value

    def increment_count(self):
        self.__count += 1

    def increment_count_by(self, count):
        self.__count += count

    def get_children(self):
        return self.__children_node

    def add_child(self, node):
        self.__index_of_child[node.__name] = len(self.__children_node)
        self.__children_node.append(node)

    def is_child_in_children(self, name):
        if name in self.__index_of_child:
            return self.__index_of_child[name]
        else:
            return -1

    def modify_time(self):
        self.__modified_time = datetime.utcnow()

    def get_child(self, index):
        return self.__children_node[index]

    def copy(self):
        return self

    def deepcopy(self):
        return deepcopy(self)


class NodeList(list):
    def item(self, index):
        if 0 <= index < len(self):
            return self[index]

    def __repr__(self):
        return '<NodeList object with %s Nodes at %s>' %(len(self), hex(id(self)))

    length = property(lambda self: len(self),
                      doc="The number of nodes in the NodeList.")

    def copy(self):
        return self

    def deepcopy(self):
        return deepcopy(self)
