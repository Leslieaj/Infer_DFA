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

    combined_node = combine_node(temp_apta, node1.get_id(), node2.get_id())

    nondeterministic_list = combined_node.nondeterministic_targets_dict()
    for nondeterministic_pair in nondeterministic_list:
        temp_node1 = temp_apta.find_node_by_id(nondeterministic_pair[0])
        temp_node2 = temp_apta.find_node_by_id(nondeterministic_pair[-1])
        _, merge_success = merge(temp_apta, temp_node1, temp_node2)
        if merge_success is False:
            return apta, False

    return temp_apta, True

    #nondeterministic = has_non_deterministic(temp_apta)


def combine_node(apta, node1_id, node2_id):
    """Combine node1 and node2, let the node having smaller id as the combined node, change the
     transitions and remove the node having bigger id. Refine the apta and return"""
    if node1_id == node2_id:
        return apta.find_node_by_id(node1_id)

    [smaller_id, bigger_id] = [node1_id, node2_id] if node1_id < node2_id else [node2_id, node1_id]
    keep_node = apta.find_node_by_id(smaller_id)
    remove_node = apta.find_node_by_id(bigger_id)

    remove_node_type = remove_node.get_nodetype()
    if remove_node_type != NodeType.unknown:
        keep_node.set_nodetype(remove_node_type)

    keepnode_in_trans_len = len(keep_node.get_in_trans())
    if keepnode_in_trans_len:
        for in_tran in remove_node.in_trans:
            in_tran.set_targetid(smaller_id)
            apta.del_tran_by_id(in_tran.get_id())
            for keep_in_tran in keep_node.in_trans:
                if in_tran.get_sourceid() == keep_in_tran.get_sourceid() and \
                    in_tran.get_label() == keep_in_tran.get_label() and \
                    in_tran.get_targetid() == keep_in_tran.get_targetid():
                    if keep_in_tran.get_id() > in_tran.get_id():
                        keep_in_tran.set_id(in_tran.get_id())
                    break
                else:
                    keep_node.add_in_tran(in_tran)
                    apta.add_transition(in_tran)
                    break
    else:
        keep_node.in_trans.extend(remove_node.in_trans)

    for out_tran in remove_node.out_trans:
        out_tran.set_sourceid(smaller_id)
        apta.del_tran_by_id(out_tran.get_id())
        apta.add_transition(out_tran)
    #keep_node.in_trans.extend(remove_node.in_trans)
    keep_node.out_trans.extend(remove_node.out_trans)
    apta.del_node_by_id(bigger_id)

    apta.show_apta_info()
    print "*****************************************************************\n"
    return keep_node

#def has_non_deterministic(temp_apta):
    #return 0
