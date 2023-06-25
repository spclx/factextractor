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


def facts_for_annotation(G, gender, most_places):
    '''
    Собирает лист из фактов и его даты упоминания
    '''
    res = Counter()
    for key, value in G.nodes.data():
            if value.get('group') == 'Category_word':
                res[key] = len(G[key])
    facts = [s for i in Counter(res).keys() for s in G.successors(i)]
    
    res = []
    for fact in facts:
        if wt.get_fact_to_annotation(fact, gender, most_places):
                date = [i for i in G.predecessors(fact) if G.nodes()[i].get('group') == 'Date'][0]
                res.append((date, fact))
    return res


def annotation(G, gender):
    dates = dates_of_Diary_writing(G)
    most_places = most_visited_places(G)
    facts = facts_for_annotation(G, gender, most_places)

    facts = ', '.join([f"{fact[1].lower()} ({fact[0]})" for fact in facts])

    annotation = f'{wt.get_noun(gender).title()} этого дневника {wt.gender_transformer("вести", gender)} его с {dates[0]} по {dates[1]}. Наиболее часто {wt.get_pronoun(gender)} {wt.gender_transformer("описывал", gender)} {wt.inflector(most_places[0], "accs")}, {wt.inflector(most_places[1], "accs")} и {wt.inflector(most_places[2], "accs")}.\n\nВ дневнике упоминается, как {wt.get_noun(gender)} {facts}.'

    return annotation