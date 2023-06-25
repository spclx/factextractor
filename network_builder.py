import networkx as nx


def build_graph(df):
    G = nx.Graph()

    # Связывание дат 
    for previous, current in zip(df['date_start'], df['date_start'][1:]):
        G.add_node(previous, group="Date", color = "blue")
        G.add_node(current, group="Date", color = "blue")
        G.add_edge(previous, current)

    # Добавление связей дат и фактов, фактов и слов
    for index, row in df[['date_start', 'loc_facts']].iterrows():
        for fact in row['loc_facts']:
            G.add_node(fact[0], group="Category_word", color = "green")
            G.add_node(fact[1], group="Fact", color = "red")
            G.add_edge(row['date_start'], fact[1])
            G.add_edge(fact[0], fact[1])

    return G