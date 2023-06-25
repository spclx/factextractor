'''
Методы преобразования слов для аннотаций
'''
import pymorphy2
from collections import Counter

morph = pymorphy2.MorphAnalyzer()

# Определение пола автора по тексту
def get_gender(tokens):
    '''
    Определение пола автора по тексту

    Возвращает ``Fem`` — женский род, ``Masc`` — мужской род.
    '''
    gender = []
    for i in [token for sent in tokens for token in sent]:
        for token in i:
            if token.feats.get('Gender') and token.pos == 'VERB':
                gender.append(token.feats.get('Gender'))
    return Counter(gender).most_common(1)[0][0]

def inflector(word, case):
    '''
    Склонение существительных по падежам.

    word : существительное

    case : падеж

    `nomn` – именительный
    `gent` — родительны
    `datv` — дательный
    `accs` — винительный
    `ablt` — творительный
    `loct` — предложный
    '''
    return morph.parse(word)[0].inflect({case}).word


def gender_transformer(verb, gender):
    '''
    Преобразование глагола в нужный род прошедшего времени
    '''
    # Преобразование формата рода Natasha к pymorphy2
    if gender == 'Fem' : gender = 'femn'
    else: gender = 'masc'

    # Если автор пишет о себе в первом лице "Я пишу..."
    # if {'1per'} in morph.parse(verb)[0].tag:
    for w in morph.parse(verb)[0].lexeme:
        if {gender, 'past', 'VERB'} in w.tag: 
            return w.word



