import networkx as nx
from collections import Counter
import word_transformations as wt
import sentiment_parser as sp
# import app


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

    # Добавление связей даты записи с сентиментом
    for index, row in df[['date_start', 'sent_index']].iterrows():
        G.add_node(sp.get_most_sentiment([row['sent_index']]), group="Sentiment", color = "pink")
        G.add_edge(row['date_start'], sp.get_most_sentiment([row['sent_index']]))
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

def sentiment_of_date(G):
    sentiment = dict()
    sentiment['positive'] = [date for date in G.predecessors('positive')]
    sentiment['negative'] = [date for date in G.predecessors('negative')]
    sentiment['neutral'] = [date for date in G.predecessors('neutral')]
    return sentiment


def constuct_fact_for_annotation(facts, sentiment, gender, locations):
    '''
    Собирает из отобранных фактов текст для аннотации.
    '''
    prompts = [f'В записях с преимущественно положительной тональностью {wt.get_noun(gender)} {wt.gender_transformer("писал", gender)} как {wt.get_pronoun(gender)}',
               f'Также в дневнике описывается, как {wt.get_pronoun(gender)}']
    

    positive_facts = []
    negative_facts = []
    if sentiment['positive']:
        for date in sentiment['positive']:
            for fact in facts:
                if date == fact[0]:
                    positive_facts.append(f"{wt.transform_fact(locations, fact[1], gender).lower()} ({fact[0]})")
    if sentiment['negative']:
        for date in sentiment['negative']:
            for fact in facts:
                print(fact[1])
                if date == fact[0]:
                    negative_facts.append(f"{wt.transform_fact(locations, fact[1], gender).lower()} ({fact[0]})")
    if sentiment['neutral']:
        for date in sentiment['neutral']:
            for fact in facts:
                print(fact[1])
                if date == fact[0]:
                    negative_facts.append(f"{wt.transform_fact(locations, fact[1], gender).lower()} ({fact[0]})")
    text = ''
    if positive_facts:
        text += f'{prompts[0]} {", ".join(positive_facts)}.'
    if negative_facts:
        text += f'\n\n{prompts[1]} {", ".join(negative_facts)}.'
    return text

def annotation(G, gender, locations):
    dates = dates_of_Diary_writing(G)
    most_places = most_visited_places(G)
    facts = facts_for_annotation(G, gender, most_places)
    sentiment = sentiment_of_date(G)

    # facts = ', '.join([f"{fact[1].lower()} ({fact[0]})" for fact in facts])
    # facts = ''

    annotation = f'{wt.get_noun(gender).title()} этого дневника {wt.gender_transformer("вести", gender)} его с {dates[0]} по {dates[1]}. Наиболее часто {wt.get_pronoun(gender)} {wt.gender_transformer("описывал", gender)} {wt.inflector(most_places[0], "accs")}, {wt.inflector(most_places[1], "accs")} и {wt.inflector(most_places[2], "accs")}.\n\n{constuct_fact_for_annotation(facts, sentiment, gender, locations)}'

    return annotation