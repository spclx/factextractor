import networkx as nx
from collections import Counter
import word_transformations as wt


def build_graph(df):
    G = nx.DiGraph()

    # Связывание дат 
    for previous, current in zip(df['date_start'], df['date_start'][1:]):
        G.add_node(previous, group="Date", color = "blue")
        G.add_node(current, group="Date", color = "blue")
        G.add_edge(previous, current)

    # Добавление связей дат и фактов, фактов и слов
    for index, row in df[['date_start', 'locations']].iterrows():
        for fact in row['locations']:
            G.add_node(fact[0], group="Category_word", color = "green")
            G.add_node(fact[1], group="Fact", color = "red")
            G.add_edge(row['date_start'], fact[1])
            G.add_edge(fact[0], fact[1])

    return G


def dates_of_Diary_writing(G):
    dates = [key for key, value in G.nodes.data() if value.get('group') == 'Date']
    start = ''
    stop = ''
    for d in dates:
        if not [i for i in G.predecessors(d)]:
            start = d
        elif not [i for i in G.successors(d) if G.nodes.data()[i]['group'] == 'Date']:
            stop = d
    return (start, stop)


def most_visited_places(G):
    res = Counter()
    for key, value in G.nodes.data():
        if value.get('group') == 'Category_word':
            res[key] = len(G[key])
    return [i[0] for i in Counter(res).most_common(3)]


def fact_to_annotation(fact, gender, most_mentioned_word):
    '''
    Отбор фактов в аннотацию

    Пока работает, если глагол в нужном лице и роде.
    '''
    flag = False
    for word in fact.split(' '):
        for form in morph.parse(word):
            # Если глагол прошедшего времени
            if {gender, 'VERB'} in form.tag:
                flag = True
            # Если глагол от "первого лица"
            if {'1per', 'sing', 'VERB'} in form.tag:
                flag = True
            if form.normal_form in most_mentioned_word:
                return False
    return flag

