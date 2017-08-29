"""test script for APTA"""

from apta import APTA, TrainWord, WordType

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
    s_pos = ["abaa", "bb", "a"]
    s_neg = ["abb", "b"]
    train_pos = buildword(s_pos, WordType.pos)
    train_neg = buildword(s_neg, WordType.neg)
    apta = APTA()
    apta.construct(train_pos, train_neg)
    apta.show_apta_info()

if __name__ == '__main__':
    main()
