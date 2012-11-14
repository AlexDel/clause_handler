# coding=utf-8

def test():
    #берем тесты из csv-файла
    tests = []
    for row in csv.reader(open('test_set/DB_1000.csv'), delimiter=';'):
    #переводим в байты из кодировки cp1251
        tests.append(tuple([r.decode('utf8') for  r in row]))
    return tests

o = 0
for t in tests[1:]:
    s1 = split_to_clauses(sentence = t[1], language='ru')
    s2 = split_to_clauses(sentence = t[0], language='en')
    if len(s2['clauses']) > 1:
        print str(len(s2['clauses'])) + str(s2['clauses'])
        for i,s in enumerate(s1['clauses']):
            print i
            print s.encode('utf8')
        print '\n'
        o += 1

print o