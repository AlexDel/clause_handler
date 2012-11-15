# coding=utf-8
import english_handler, russian_handler, normalizer, csv, json


def split_to_clauses(enter_sentence):

    """
    метод разбивает предложение на клаузы,
    выбирая по языку нужные обработчики
    принимает на вход переменную в json следующего вида:

    {'language':  'sentence''}
    где
        'language' - язык предлоэения,
        'sentence' - текст предложения

    :rtype : json
    {{'clauses':[clause1,clause2 ]},'tense':'foo','type':'bar'}
    где
        clauses - полученные при извлечении клаузы
        tense - время пердложения
        type - тип предложения, coord или subord

    """

    sentence = json.loads(enter_sentence)

    if sentence.key() == u'ru':

        output = russian_handler.process(sentence['ru'])

    elif sentence.key() == u'en':

        output = english_handler.process(sentence['en'])
    else:
        output = None

    output['language'] = sentence['language']

    print json.dumps(output)
    return json.dumps(output)


def check_stream(stream_a, stream_b):
    """
    метод осуществояет проверку, и возвращает код ошибки
    """

    response = {'code':0,'description':'Unknown error'}

    if len(stream_a) == 1 or len(stream_b) == 1:
        response['code'] = 2
        response['description'] = 'No clauses for matching found'


    elif len(stream_a) != len(stream_b):
        response['code'] = 3
        response['description'] = "Clauses' size don't match"

    #elif stream_b['type'] != stream_a['type']:
     #   response['code'] = 4
      #  response['description'] = "Types of clauses' don't match"

    #elif stream_a['type']  == 'subord' and (stream_b['tense'] == 'past' or stream_a['tense'] == 'past'):
     #   response['code'] = 5
      #  response['description'] = "Main clause contain past tense."

    elif len(stream_a) == len(stream_b):
        response['code'] = 1
        response['description'] = 'Clauses are found and ready to be matched'

    return response


def merge_clauses(sentences):

    """
    этот метод получает json в виде списка "язык-предлоэение"
    {
        'ru':russian_sentence
        'en':english_sentence
    }

    возращает список клауз + код ответа
    {
        'clauses':
        [{'ru':rus_clause_i.'en':eng_clause_i}]
        [{'ru':rus_clause_i.'en':eng_clause_i}]
        [{'ru':rus_clause_i.'en':eng_clause_i}]
        response:
            {code:0,
            description:''}

    }

    """
    input = json.loads(sentences)

    sent_rus = input['ru']
    sent_en = input['en']

    sent1 = json.loads(split_to_clauses(json.dumps({'ru':sent_rus})))
    sent2 = json.loads(split_to_clauses(json.dumps({'en':sent_en})))

    checking = check_stream(sent1, sent2)


    if checking['code'] == 1:
        zipped_clauses =  zip(sent1['clauses'], sent2['clauses'])
    else:
        zipped_clauses = None

    #пока что zipped_clauses[i][0] - русские клаузы,  zipped_clauses[i][2] - английские
    #со временем необходимо переделать метод под произвольные языки

    #инициализируем переменную для вывода
    output = {'clauses':[],'response':checking}

    if(zipped_clauses):
        for pairs in zipped_clauses:
            output['clauses'].append({'ru':normalizer.normalize(pairs[0]),'en':normalizer.normalize(pairs[1])})
    else:
        output['clauses'] = None

    print json.dumps(output)
    return json.dumps(output)
