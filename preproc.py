from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    Doc
)


segmenter = Segmenter()
morph_vocab = MorphVocab()
morph_tagger = NewsMorphTagger(NewsEmbedding())
syntax_parser = NewsSyntaxParser(NewsEmbedding())

def text_preproc(df):
    patterns = [r'<com id=\d+"/>', r'<com id="\d+"/>', r'<\w+>', r'<\/\w+>', r'<\w+\s/>', '\*', '#', '\[', '\]']
    for pattern in patterns:
        df['text'] = df['text'].str.replace(pattern, '', regex=True)
    return df


def tokenizing(text):
    doc = Doc(text)
    doc.segment(segmenter)
    tokens = []
    for sent in doc.sents:
        sent = Doc(sent.text)
        sent.segment(segmenter)
        sent.parse_syntax(syntax_parser)
        sent.tag_morph(morph_tagger)
        for token in sent.tokens:
            token.lemmatize(morph_vocab)
        tokens.append(sent.tokens)
    return tokens


def get_all_lemmas(tokens):
    return [token.lemma for sent in tokens for token in sent]


def get_set_all_lemmas(tokens):
    return set(get_all_lemmas(tokens))


def get_set_sent_lemmas(sent_tokens):
    return set([token.lemma for token in sent_tokens])


def get_sent_tokens(sent_tokens):
    return [token for token in sent_tokens]