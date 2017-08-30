""" functions : state-merging methords of different frammework"""
import copy
from apta import APTA, Node
from enumtype import NodeType

def merge(apta=None, node1=None, node2=None):
    if isinstance(apta, APTA) or isinstance(node1, Node) or isinstance(node2, Node):
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

    replace_node_by_combined_node(temp_apta, node1, node2, combined_node)

    #nondeterministic = has_non_deterministic(temp_apta)


def replace_node_by_combined_node(apta, node1, node2, combined_node):
    node1_id = node1.get_id()
    node2_id = node2.get_id()
    if node1_id == node2_id:
        combined_node = node1
        return combined_node
    combined_node.set_id(node1_id if node1_id < node2_id else node2_id)
    combined_node.set_in_trans(node1.get_in_trans() + node2.get_in_trans())
    combined_node.set_out_trans(node1.get_out_trans() + node2.get_out_trans())

#def has_non_deterministic(temp_apta):
    #return 0
