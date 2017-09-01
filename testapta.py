"""test script for APTA"""

from apta import APTA, TrainWord, WordType
from statemerge import merge

def buildword(stringlist, traintype):
    if len(stringlist) == 0:
        return None
    else:
        trainlist = []
        for word in stringlist:
            training = TrainWord(word)
            training.set_wordtype(traintype)
            trainlist.append(training)
        return trainlist

def main():
    s_pos = ["abaa", "a", "bb"]
    s_neg = ["abb", "b"]
    train_pos = buildword(s_pos, WordType.pos)
    train_neg = buildword(s_neg, WordType.neg)
    apta = APTA(train_pos, train_neg)
    apta.show_apta_info()
    print "*****************************************************************\n"
    node1 = apta.find_node_by_id(0)
    node2 = apta.find_node_by_id(1)
    temp, flag = merge(apta, node1, node2)
    print flag
    temp.show_apta_info()
    #node1 = temp.find_node_by_id(2)
    #node2 = temp.find_node_by_id(5)
    #temp1, flag1 = merge(temp, node1, node2)

    # apta.show_apta_info()
    # print "*****************************************************************\n"
    # if flag is True:
    #     temp.show_apta_info()
    # print "*****************************************************************\n"
    # if flag1 is True:
    #     temp1.show_apta_info()

if __name__ == '__main__':
    main()
