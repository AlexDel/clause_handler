# -*- coding: utf-8 -*-
import nltk, re, pymorphy, csv
from nltk.tokenize import RegexpTokenizer

#подключаем морфологию
from pymorphy import get_morph
morf_storage = 'morf_storage/ru.shelve'
morph = get_morph(morf_storage, backend='shelve')


def declause(sentence):
    #смотрим является, ли предложение content-clause или нет (есть ли союз "что")
    if re.search(u',и?\s*что', sentence):
        regexp_pattern = u',и?\s*что'

        #создаем токенайзер с заданой регуляркой
        clauses = RegexpTokenizer(regexp_pattern, gaps = True).tokenize(sentence)

        #для первой клаузы(главной, ставим маркер <noncont> каждой вложенной content-клаузы в начале добавляем тэг <content>
        return [u'<noncont>' + clauses[0]] + [u'<content>' + c for c in clauses[1:]]

    elif re.search(u",\s*(и)|(но)|(а)|(или)\s+", sentence):

        # разделяем предложение на noncontent-клаузы по границам сочинительных союзов
        regexp_pattern = u',\s*((и)|(но)|(а)|(или)|(потому что))\s+'

        #для для каждого не content-<coord>
        clauses = RegexpTokenizer(regexp_pattern, gaps = True).tokenize(sentence)
        return [u'<noncont>' + c for c in clauses]
    else:
        return ''

def search_core(clause):
    #ищем синтаксическое ядро в клаузе
    #бъем на слова
    words = RegexpTokenizer(u"[A-Za-zА-Яа-я]+").tokenize(clause)

    processed_clause = []
    #перебираем слова и анализируем
    for w in words:
        w_info = morph.get_graminfo(w.upper())

        #запоминаем все полученные разборы
        morf_info = [(i['class'],i['info']) for i in w_info]
        processed_clause.append([w, morf_info])
        #на выходе мы получаем список списков.
    #каждый список второго уровня имеет вид [токен, (кортеж с вариантами разбора 1)(кортеж с вариантами разбора 2)]

    #Инициализируем переменные
    has_predicate = False
    has_subject = False
    subject_position = []
    predicate_position = []
    #ищем основу предложения и извлекаем линейную позицию токена
    for i, token in enumerate(processed_clause):
        #поддержка английских имен собственных в предложениях (Facebook, Oracle etc)
        if re.search(u'[a-zA-z]+', token[0]):
            has_subject = True
            subject_position.append(i)
        for morf in token[1]:
            if morf[0] == u"Г":
                has_predicate = True
                predicate_position.append(i) #берем списком, чтобы взять превое соотвествие
            if morf[1].count(u"им"):
                has_subject = True
                subject_position.append(i) #берем списком, чтобы взять превое соотвествие

    #есть сказуемое, есть подлежащее и оно предшествует сказуемомоу
    is_a_clause = has_predicate and has_subject and (subject_position[0] <= predicate_position[0])

    return  is_a_clause

def get_tense(verb):
    #этот метод использует морфологический анализатор и возвращает время глагола
    info = morph.get_graminfo(verb)
    print info[0]['info'].encode('cp1251')
    for var in info:
        #если один из вариантов - разбора глагол, возвращаем второй эл-т ключа ['info'] - время (буд, нст, прш)
        if var['class'] == u'Г':
            return var['info'][1]

def process(sentence):
#   этот метод должен интегрировать предыдущие функции, решать годитс ли оно для обработки
#   и возвращать поделенное предложение. При проверке проверяем соотвествует ли число поделенных клауз,
#   числу валидизированных клауз. Если нет, возвращаем None

    result = []
    proccessed_clauses = declause(sentence)

    #если в клаузе определяется клауза, добавляем в список, если нет, конкатенируем с предыдущим
    for sent in proccessed_clauses:
        if search_core(sent):
            result.append(sent)
        else:
            if len(result) == 0:
                result.append(sent)
            else:
                result[-1] + sent
    if len(proccessed_clauses) == len(result):
        return result
    else:
        return sentence
