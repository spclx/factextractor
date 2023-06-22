import json
import os
import preproc
from collections import Counter, deque
import numpy as np

# Находит токен целевого слова по концу слова
def find_need_word_by_lemma(tokens, word):
    res = []
    for token in tokens:
        if token.lemma == word:
            res.append(token.stop)
    return res


def find_first(tokens, stop):
    for token in tokens:
        if token.stop == stop:
            return (token.id, token.rel)
        

# Находит связанное слово
def find_related_word(scenario, id, r1, r2, rel_ids, rels, head_ids, words):
    if scenario == 0: # Нам известен 0 элемент в кортеже
        try:
            for i in rel_ids.get(id):
                if rels[i] == r2:
                    if (r2 == 'advmod') & (words.get(i) != 'не'):
                        continue
                    return i
        except: 
            return '1_0'
    elif scenario == 1: # Нам известен 1 элемент в кортеже
        for i in r1:
            if rels.get(head_ids[id]) == i:
                return head_ids[id]

    return '1_0'

# Собирает факт по целевому слову
def construct_fact(tokens, stop, category):
    words = dict()
    head_ids = dict()
    rels = dict()
    rel_ids = dict()

    instructions = get_insructions(category)

    for token in tokens:
        words[token.id] = token.text
        head_ids[token.id] = token.head_id
        if rel_ids.get(token.head_id):
            rel_ids[token.head_id].append(token.id)
        else:
            rel_ids[token.head_id] = [token.id]
        rels[token.id] = token.rel
    
    fact = deque()
    first_word = find_first(tokens, stop)
    id = first_word[0]
    fact.append(words[first_word[0]])

    breaker = False 

    if instructions.get(first_word[1]):
        for instruction in instructions[first_word[1]]:
            for i in instruction:
                related_word = find_related_word(i[2], id, i[0], i[1], rel_ids, rels, head_ids, words)
                #print(related_word)
                if (related_word == '1_0') & (instruction.index(i) == 1):
                    break
                elif related_word == '1_0':
                    pass
                elif i[2] == 0:
                    fact.appendleft(words[related_word])
                else: 
                    fact.appendleft(words[related_word])
                    id = related_word

                if instruction.index(i) == len(instruction) - 1:
                    breaker = True
            
            if breaker:
                break
        
        if len(fact) == len(set(fact)):
            if len(fact) > 1:
                return ' '.join(fact)
            else: pass
        else: 
            fact.popleft()
            return ' '.join(fact)
    else: pass


# Поскольку в одном предложении могут быть несколько целевых слов, которые могут быть связаны, эта функция провеярет, не являются факт сокращённой копией прошлого факта
def cheker_fact(previous_fact, new_fact):
    previous_fact = set(previous_fact.split(' '))
    new_fact = set(new_fact.split())

    if len(previous_fact & new_fact) != len(new_fact):
        return True
    else:
        return False
    

SCRIPT_DIR = os.path.dirname(__file__)

def get_insructions(category):
    with open(f'{SCRIPT_DIR}/{category}/instructions.json') as f:
        return json.load(f)   
    

def get_category_words(category):
    return set(open(f'{SCRIPT_DIR}/{category}/words.txt', encoding='utf8').read().split('\n'))


def get_facts(tokens, category):
    facts = []
    for sent in tokens:
        sent_tokens = preproc.get_sent_tokens(sent)
        set_lemmas = preproc.get_set_sent_lemmas(sent)
        res = set_lemmas & get_category_words(category)
        if res:
            for w in res:
                for word in find_need_word_by_lemma(sent_tokens, w):
                    fact = construct_fact(sent_tokens, word, category)
                    if fact: 
                        facts.append(fact)
    return facts


def get_mentioned_words(tokens, category):
    lemmas = preproc.get_all_lemmas(tokens)
    res = set(lemmas) & get_category_words(category)
    if res:
        return Counter([lemma for lemma in lemmas if lemma in res])
    else:
        return Counter()

def get_most_mentioned_words(mentioned_words):
    return mentioned_words.sum().most_common(3)
