# -*- coding: utf-8 -*-
import nltk, re, csv
from nltk.tokenize import RegexpTokenizer

#подргужаем морфологию
from cPickle import load
morf_storage = 'morf_storage/brill.pkl'

grammar1 = r"""
            NP:
                {<AT>?<CD>*<PRP$>?<AP>?<DT|NN.*>+}
                <N.*>{}<N.*>
                {<N.*><CC>?<N.*>} #?
                {<PRP>}
                {<PPS>}
                {<VBG>}
                {<AP>?<NP>}
            AP:
                {<JJR>?<JJ>+}
                {<A.*><CC>?<A.*>}
            PP:
                {<IN><NP>}
                {<P.*><P.*>}
            VP:
                {<MD>*<RB>*<VB.?><NP|PP|CLAUSE>*<RB>*}
                {<V.*><CC>?<V.*>}
                {<BEZ><AP>?}
            CONJ:
                <NP><PP>?<VP><PP>?{(<CC>|<IN>)}<NP><PP>?<VP><PP>?
                        
"""




def pos_tag(sent):

    input = open(morf_storage, 'rb')
    tagger = load(input)
    input.close()
    tagged_s = tagger.tag(sent.split())

    #подчинительные союзы
    sub_conj = ['that','who','what','why','when']

    for i, e in enumerate(tagged_s):
        if re.match(r'V.*',tagged_s[i-1][1]) and tagged_s[i][0] in sub_conj:
            #claused_sent['type'] = 'content'
            tagged_s[i] = (tagged_s[i][0], 'CC')

    return tagged_s


def define_sentence_props(sentence):
    """
    эта функция определяет параметры главоного (первого) предложения, его время и
    """

    sent_props = {'type':'undefined', 'tense':'present'}
    tagged_s = pos_tag(sentence)

    #подчинительные союзы
    sub_conj = ['that','who','what','why','when']
    past_tense_tags = ['VBD','BED','BEDZ','HVD','DOD']

    for i, e in enumerate(tagged_s):
        if re.match(r'V.*',tagged_s[i-1][1]) and tagged_s[i][0] in sub_conj:
            #claused_sent['type'] = 'content'
            sent_props['type'] = 'subord'
            main_clause = tagged_s[0:i]
            break

    for word,tag in main_clause:
        if tag in past_tense_tags:
            sent_props['tense'] = 'past'

    return sent_props


def make_parse(tagged_s, grammar = grammar1):
    #готовим парсер

    parser = nltk.RegexpParser(grammar,loop=4)
    parsed_s = parser.parse(tagged_s)
    return parsed_s


def flatten(parsed_s):
    #инициализируем строку
    bounded_sent = ''

    #перебираем верхние уровни древа.
    #если встречаем союз (CONJ) присоединяем
    #если встречается не поддрево, обрабатываем как кортеж
    for subtree in parsed_s:
        if isinstance(subtree, tuple):
            bounded_sent += ' ' + subtree[0] + ' '
        elif subtree.node == 'CONJ':
            bounded_sent += '|'
        else:
            bounded_sent += ' '.join([w for w, t in subtree.leaves()]) + ' '

    return bounded_sent.split('|')

def search_core(clause):
    clause_tree = make_parse(pos_tag(clause), grammar1)

    np_position = 0
    vp_position = 0

    for i, subtree in enumerate(clause_tree):
        if isinstance(subtree, tuple):
            pass
        elif subtree.node == 'NP':
            np_position = i
            break

    for i, subtree in enumerate(clause_tree):
        if isinstance(subtree, tuple):
            pass
        elif subtree.node == 'VP':
            vp_position = i
            break

    if np_position == True & np_position == True & np_position < vp_position:
        return True
    else:
        return False


def declause(sentence):

    if re.search(u',\s*(and)|(but)|(yet)|(or)\s+', sentence):

        # разделяем предложение на noncontent-клаузы по границам сочинительных союзов
        regexp_pattern = u',\s*(and)|(but)|(yet)\s+'
        clauses = RegexpTokenizer(regexp_pattern, gaps = True).tokenize(sentence)

        good_clauses = []

        for c in clauses:
            if search_core(c):
                good_clauses.append(c)
            else:
                return [sentence]

        return good_clauses

    else:
        return [sentence]

def process(sent):
    s_prime = flatten(make_parse(pos_tag(sent), grammar1))

    if len(s_prime) < 2:
        return declause(s_prime[0])
    else:
        return s_prime


#def test():
#    #берем тесты из csv-файла
#    tests = []
#    for row in csv.reader(open('/home/verbalab/test-set.csv'), delimiter=';'):
#    #переводим в байты из кодировки cp1251
#        tests.append(tuple([r.decode('cp1251') for  r in row]))
#    return tests
#
#tests = test()

#готовим тесты





