""" functions : state-merging methords of different frammework"""

from apta import APTA, Node
from enumtype import NodeType
import copy

def merge(apta=None, node1=None, node2=None):
    if isinstance(apta, APTA) or isinstance(node1, Node) or isinstance(node1, Node):
        return None, False

    node1_type = node1.get_nodetype()
    node2_type = node2.get_nodetype()
    if (node1_type == NodeType.accepting and node2_type == NodeType.rejecting) or \
       (node1_type == NodeType.rejecting and node2_type == NodeType.accepting):
        return apta, False

    temp_apta = copy.deepcopy(apta)
    combined_node = Node(-1)
    if node1_type == NodeType.rejecting or node2_type == NodeType.rejecting:
        combined_node.set_nodetype(NodeType.rejecting)
    if node1_type == NodeType.accepting or node2_type == NodeType.accepting:
        combined_node.set_nodetype(NodeType.accepting)
    replace_node_by_combined_node(node1, node2, combined_node)

def replace_node_by_combined_node(node1, node2, combined_node):
    pass
