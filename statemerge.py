""" functions : state-merging methords of different frammework"""
import copy
from apta import APTA, Node
from enumtype import NodeType

def merge(apta=None, node1=None, node2=None):
    """state merging function"""
    if not (isinstance(apta, APTA) or isinstance(node1, Node) or isinstance(node2, Node)):
        return apta, False

    node1_type = node1.get_nodetype()
    node2_type = node2.get_nodetype()
    if (node1_type == NodeType.accepting and node2_type == NodeType.rejecting) or \
       (node1_type == NodeType.rejecting and node2_type == NodeType.accepting):
        return apta, False

    temp_apta = copy.deepcopy(apta)

    combine_node(temp_apta, node1.get_id(), node2.get_id())

    return temp_apta, True

    #nondeterministic = has_non_deterministic(temp_apta)


def combine_node(apta, node1_id, node2_id):
    """Combine node1 and node2, let the node having smaller id as the combined node, change the
     transitions and remove the node having bigger id. Refine the apta and return"""
    if node1_id == node2_id:
        return apta

    [smaller_id, bigger_id] = [node1_id, node2_id] if node1_id < node2_id else [node2_id, node1_id]
    keep_node = apta.find_node_by_id(smaller_id)
    remove_node = apta.find_node_by_id(bigger_id)

    remove_node_type = remove_node.get_nodetype()
    if remove_node_type != NodeType.unknown:
        keep_node.set_nodetype(remove_node_type)

    for in_tran in remove_node.in_trans:
        in_tran.set_targetid(smaller_id)
        apta.del_tran_by_id(in_tran.get_id())
        apta.add_transition(in_tran)
    for out_tran in remove_node.out_trans:
        out_tran.set_sourceid(smaller_id)
        apta.del_tran_by_id(out_tran.get_id())
        apta.add_transition(out_tran)
    keep_node.in_trans.extend(remove_node.in_trans)
    keep_node.out_trans.extend(remove_node.out_trans)
    apta.del_node_by_id(bigger_id)

    return apta

#def has_non_deterministic(temp_apta):
    #return 0
