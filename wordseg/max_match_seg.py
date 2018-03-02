#!/usr/bin/env python
#coding=utf-8


def load_vocab(vocabfile, coding='utf-8'):
    """ 加载词典 """
    vocabdict = dict()
    vocab_maxlen = 1
    for word in open(vocabfile):
        word = word.strip('\n').decode(coding, 'ignore')
        vocabdict[word] = 1
        if len(word) > vocab_maxlen:
            vocab_maxlen = len(word)
    return vocabdict, vocab_maxlen

def pre_match_seg_imp(sentence, vocabdict, vocab_maxlen=6):
    """ 前向最大匹配实现 """
    seglist = list()
    while len(sentence) > 0:
        if len(sentence) == 1:
            seglist.append(sentence)
            break
        termlen = min(len(sentence), vocab_maxlen)
        for end in xrange(termlen, 0, -1):
            term = sentence[:end]
            if term in vocabdict:
                seglist.append(term)
                break
        if end == 1:
            seglist.append(sentence[0])
        sentence = sentence[end:]
    return seglist
    def pre_match_seg(corpusfile, vocabfile, coding='utf-8', sep=' '):
    """ 前向最大匹配 """
    vocabdict, vocab_maxlen = load_vocab(vocabfile)
    for line in open(corpusfile):
        sentence = line.strip('\n').decode(coding, 'ignore')
        seglist = pre_match_seg_imp(sentence, vocabdict, vocab_maxlen)
        print sep.join(seglist).encode(coding, 'ignore')

def back_match_seg_imp(sentence, vocabdict, vocab_maxlen=6):
    seglist = list()
    while len(sentence) > 0:
        if len(sentence) == 1:
            seglist.append(sentence)
            break
        termlen = min(len(sentence), vocab_maxlen)
        for start in xrange(termlen, 0, -1):
            term = sentence[0-start : ]
            if term in vocabdict:
                seglist.append(term)
                break
        if start == 1:
            seglist.append(sentence[-1])
        sentence = sentence[: 0-start]
    seglist.reverse()
    return seglist

def back_match_seg(corpusfile, vocabfile, coding='utf-8', sep=' '):
    vocabdict, vocab_maxlen = load_vocab(vocabfile)
    for line in open(corpusfile):
        sentence = line.strip('\n').decode(coding, 'ignore')
        seglist = back_match_seg_imp(sentence, vocabdict, vocab_maxlen)
        print sep.join(seglist).encode(coding, 'ignore')
        
def bi_direction_match_result_choose(seglist, rseglist):
    """ 1.如果正反向分词结果词数不同，则取分词数量较少的那个。
        2.如果分词结果词数相同
            a.分词结果相同，就说明没有歧义，可返回任意一个。
            b.分词结果不同，返回其中单字较少的那个。
    """
    if len(seglist) != len(rseglist):
        return seglist if len(seglist) < len(rseglist) else rseglist
    if seglist == rseglist:
        return rseglist
    pre_single_cnt = len([term for term in seglist if len(term)==1])
    back_single_cnt = len([term for term in rseglist if len(term)==1])
    return seglist if pre_single_cnt < back_single_cnt else rseglist

def bi_direction_match_seg(corpusfile, vocabfile, coding='utf-8', sep=' '):
    vocabdict, vocab_maxlen = load_vocab(vocabfile)
    for line in open(corpusfile):
        sentence = line.strip('\n').decode(coding, 'ignore')
        seglist = pre_match_seg_imp(sentence, vocabdict, vocab_maxlen)
        rseglist = back_match_seg_imp(sentence, vocabdict, vocab_maxlen)

        choose_seglist = bi_direction_match_result_choose(seglist, rseglist)
        print sep.join(choose_seglist).encode(coding, 'ignore')
