""" construct augmented prefix tree acceptor."""

# import copy
from enumtype import NodeType, NodeColor, WordType

class Node(object):
    """class Node for the nodes in APTA"""
    def __init__(self, nodeid, nodetype=NodeType.unknown, \
    nodecolor=NodeColor.white, isroot=False):
        self.nodeid = nodeid
        self.in_trans = []
        self.out_trans = []
        self.nodetype = nodetype
        self.nodecolor = nodecolor
        self.isroot = isroot

    def set_id(self, nodeid):
        self.nodeid = nodeid
    def get_id(self):
        return self.nodeid

    def add_in_tran(self, in_tran):
        #self.in_trans = self.in_trans + [in_tran]
        self.in_trans.append(in_tran)
    def remove_in_tran(self, in_tran):
        pass
    def set_in_trans(self, in_tran_list):
        self.in_trans = in_tran_list
    def get_in_trans(self):
        return self.in_trans

    def add_out_tran(self, out_tran):
        #self.out_trans = self.out_trans + [out_tran]
        self.out_trans.append(out_tran)
    def set_out_trans(self, out_tran_list):
        self.out_trans = out_tran_list
    def get_out_trans(self):
        return self.out_trans

    def set_nodetype(self, nodetype):
        self.nodetype = nodetype
    def get_nodetype(self):
        return self.nodetype

    def set_nodecolor(self, nodecolor):
        self.nodecolor = nodecolor
    def get_nodecolor(self):
        return self.nodecolor

    def set_root(self, isroot):
        self.isroot = isroot
    def is_root(self):
        return self.isroot

    def has_out_tran_by_label(self, label):
        if len(self.out_trans) == 0:
            return False, None
        else:
            for tran in self.out_trans:
                if tran.label == label:
                    return True, tran.get_targetid()
            return False, None

    def nondeterministic_targets_dict(self):
        """finding the targets of out transitions with same labels,
           it return a list [[taget_node_id,...], [target_node_id,...],...]
        """
        dictionary = {}
        nondeterministic_pair_list = []
        for tran in self.out_trans:
            dictionary[tran.get_label()] = []
        for tran in self.out_trans:
            for k in dictionary.keys():
                if tran.get_label() == k:
                    dictionary[k].append(tran.get_id())
        for k in dictionary.keys():
            if len(dictionary[k]) > 1:
                nondeterministic_pair_list.append(dictionary[k])
        return nondeterministic_pair_list

    def show_out_trans(self):
        for tran in self.get_out_trans():
            traninfo = 'tran_id: ' + str(tran.get_id()) + ' ' \
            + 'label: ' + tran.get_label() + ' ' \
            + 'source_id: ' + str(tran.get_sourceid()) + ' ' \
            + 'target_id: ' + str(tran.get_targetid()) + '\n'
            print traninfo

class Transition(object):
    """class Transition for the transitions in APTA"""
    def __init__(self, transid, label="", sourceid=None, targetid=None):
        self.transid = transid
        self.label = label
        self.sourceid = sourceid
        self.targetid = targetid

    def get_id(self):
        return self.transid
    def set_id(self, transid):
        self.transid = transid

    def get_label(self):
        return self.label
    def set_label(self, label):
        self.label = label

    def get_sourceid(self):
        return self.sourceid
    def set_sourceid(self, sourceid):
        self.sourceid = sourceid

    def get_targetid(self):
        return self.targetid
    def set_targetid(self, targetid):
        self.targetid = targetid

    def similar_to(self, transition):
        if self.get_sourceid() == transition.get_sourceid() and \
           self.get_label() == transition.get_label() and \
           self.get_targetid() == transition.get_targetid():
            return True
        return False

class TrainWord(str):
    #def __new__(cls, value):
        #return str.__new__(cls, value)
    def __init__(self, value):
        str.__init__(self, value)
        self.wordtype = WordType.unknown

    def get_wordtype(self):
        return self.wordtype
    def set_wordtype(self, wordtype):
        self.wordtype = wordtype

class APTA(object):
    """ class APTA : the augmented prefix tree acceptor for training set"""
    def __init__(self, pos_training, neg_training):
        self.root = Node(nodeid=0, isroot=True)
        self.nodeset = [self.root]
        self.transitionset = []
        self.construct(pos_training, neg_training)

    def add_node(self, node=None):
        self.nodeset.append(node)

    def del_node_by_id(self, nodeid):
        """delete a node of the apta"""
        node = self.find_node_by_id(nodeid)
        if node is None:
            return False
        else:
            self.nodeset.remove(node)
            #self.del_trans_by_nodeid(node.get_id())
            return True

    def find_node_by_id(self, nodeid):
        for node in self.nodeset:
            if nodeid == node.get_id():
                return node
        return None

    def add_transition(self, transition=None):
        self.transitionset.append(transition)

    def find_tran_by_id(self, tranid):
        for transition in self.transitionset:
            if tranid == transition.get_id():
                return transition
        return None

    def del_trans_by_nodeid(self, nodeid):
        for transition in self.transitionset:
            if transition.get_sourceid() == nodeid or transition.get_targetid() == nodeid:
                self.transitionset.remove(transition)

    def del_tran_by_id(self, tranid):
        transition = self.find_tran_by_id(tranid)
        if transition is None:
            return False
        else:
            self.transitionset.remove(transition)

    def construct(self, pos_training, neg_training):
        if len(pos_training) == 0 or len(neg_training) == 0:
            return False
        else:
            trainingset = pos_training + neg_training
            nodeid = 0
            transid = 0
            for train_string in trainingset:
                node = self.root
                i = 1
                stringlen = len(train_string)
                while i <= stringlen:
                    label = train_string[i-1]
                    haslabel, targetid = node.has_out_tran_by_label(label)
                    if not haslabel:
                        nodeid = nodeid + 1
                        transid = transid + 1
                        target = Node(nodeid)
                        transition = Transition(transid, label, node.get_id(), target.get_id())
                        node.add_out_tran(transition)
                        target.add_in_tran(transition)
                        self.add_node(target)
                        self.add_transition(transition)
                        node = target
                    else:
                        node = self.find_node_by_id(targetid)
                    i = i+1
                if train_string.get_wordtype() == WordType.pos:
                    node.set_nodetype(NodeType.accepting)
                else:
                    node.set_nodetype(NodeType.rejecting)

    # def has_nondeterministic(self):
    #     """ list like: [[...], [...], [...],...] """
    #     nondeterministic_list = []
    #     for node in self.nodeset:
    #         dictionary = node.nondeterministic_targets_dict()
    #         nondeterministic_list += dictionary.values()
    #     return nondeterministic_list

    def show_apta_info(self):
        for node in self.nodeset:
            nodeinfo = 'node_id: ' + str(node.get_id()) + ' ' \
            + 'root: ' + str(node.is_root()) + ' ' \
            + 'type: '+ NodeType.to_str(node.get_nodetype()) + '\n'
            print nodeinfo
            for tran in self.transitionset:
                if tran.get_sourceid() == node.get_id():
                    traninfo = 'tran_id: ' + str(tran.get_id()) + ' ' \
                    + 'label: ' + tran.get_label() + ' ' \
                    + 'source_id: ' + str(tran.get_sourceid()) + ' ' \
                    + 'target_id: ' + str(tran.get_targetid()) + '\n'
                    print traninfo
