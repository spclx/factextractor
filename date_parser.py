from yargy import (
    Parser,
    rule,
    and_, or_
)
from yargy.interpretation import fact
from yargy.predicates import (
    eq, gte, lte, length_eq,
    dictionary, normalized,
)
import pandas as pd


DateRange = fact(
    'DateRange',
    ['start_day', 'start_month', 'start_year', 'stop_day', 'stop_month', 'stop_year']
)
class DateRange(DateRange):
    years_collection = [1900]

    @property
    def normalized(self):
        if self.start_year != None:
            self.years_collection.append(self.start_year)
        else:
            self.start_year = self.years_collection[-1]
        
        if self.start_day == None:
            self.start_day = 0

        if self.start_month == None:
            self.start_month = 0

        if self.stop_year == None:
            self.stop_year = self.start_year
        
        if self.stop_month == None:
            self.stop_month = self.start_month
        
        if self.stop_day == None:
            self.stop_day = self.start_day

        return self
    @property
    def get_start_date(self):
        return str(self.start_year) + '-' + str(self.start_month).zfill(2) + '-' + str(self.start_day).zfill(2)
    @property
    def get_stop_date(self):
        return str(self.stop_year) + '-' + str(self.stop_month).zfill(2) + '-' + str(self.stop_day).zfill(2)

MONTHS = {
    'январь': 1,
    'февраль': 2,
    'март': 3,
    'апрель': 4,
    'май': 5,
    'июнь': 6,
    'июль': 7,
    'август': 8,
    'сентябрь': 9,
    'октябрь': 10,
    'ноябрь': 11,
    'декабрь': 12,
}


MONTHS_LATIN = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9,
    'X': 10,
    'XI': 11,
    'XII': 12
}

DAY_START = and_(
    gte(1),
    lte(31)
).interpretation(
    DateRange.start_day.custom(int)
)

DAY_STOP = and_(
    gte(1),
    lte(31)
).interpretation(
    DateRange.stop_day.custom(int)
)

MONTH_NAME_START = dictionary(MONTHS).interpretation(
    DateRange.start_month.normalized().custom(MONTHS.__getitem__)
)

MONTH_NAME_STOP = dictionary(MONTHS).interpretation(
    DateRange.stop_month.normalized().custom(MONTHS.__getitem__)
)

MONTH_LATIN_NAME_START = dictionary(MONTHS_LATIN).interpretation(
    DateRange.start_month.custom(MONTHS_LATIN.__getitem__)
)

MONTH_LATIN_NAME_STOP = dictionary(MONTHS_LATIN).interpretation(
    DateRange.stop_month.custom(MONTHS_LATIN.__getitem__)
)

MONTH_START = and_(
    gte(1),
    lte(12)
).interpretation(
    DateRange.start_month.custom(int)
)

MONTH_STOP = and_(
    gte(1),
    lte(12)
).interpretation(
    DateRange.stop_month.custom(int)
)


YEAR_START = and_(
    gte(1800),
    lte(2100)
).interpretation(
    DateRange.start_year.custom(int)
)

YEAR_STOP = and_(
    gte(1800),
    lte(2100)
).interpretation(
    DateRange.stop_year.custom(int)
)

YEAR_SHORT_START = and_(
    length_eq(2),
    gte(0),
    lte(99)
).interpretation(
    DateRange.start_year.custom(lambda _: 1900 + int(_))
)

YEAR_SHORT_STOP = and_(
    length_eq(2),
    gte(0),
    lte(99)
).interpretation(
    DateRange.stop_year.custom(lambda _: 1900 + int(_))
)

YEAR_WORD = or_(
    rule('г', eq('.').optional()),
    rule(normalized('год'))
)

PUNCT_DIVISION_DATES = or_(
    rule('-'), # дефис
    rule('—'), # короткое тире
    rule('—') # длинное тире
)

PUNCT = or_(
    rule('.'),
    rule('/')
)

DATE_RANGE = or_(
    # 1-2 января 1900
    rule(
        DAY_START,
        PUNCT_DIVISION_DATES,
        DAY_STOP,
        PUNCT.optional(),
        or_(
            MONTH_NAME_START,
            MONTH_START,
            MONTH_LATIN_NAME_START
        ),
        PUNCT.optional(),
        or_(
            YEAR_START,
            YEAR_SHORT_START
        ).optional(),
        YEAR_WORD.optional()
    ),
    # 1 января - 2 февраля 1900
    rule(
        DAY_START,
        PUNCT.optional(),
        or_(
            MONTH_NAME_START,
            MONTH_START,
            MONTH_LATIN_NAME_START
        ),
        PUNCT_DIVISION_DATES,
        DAY_STOP,
        PUNCT.optional(),
        or_(
            MONTH_NAME_STOP,
            MONTH_STOP,
            MONTH_LATIN_NAME_STOP
        ),
        PUNCT.optional(),
        or_(
            YEAR_START,
            YEAR_SHORT_START
        ).optional(),
        YEAR_WORD.optional()
    ),
    # 1 января 1900 - 2 февраля 1901
    rule(
        DAY_START,
        PUNCT.optional(),
        or_(
            MONTH_NAME_START,
            MONTH_START,
            MONTH_LATIN_NAME_START
        ),
        PUNCT.optional(),
        or_(
            YEAR_START,
            YEAR_SHORT_START
        ),
        PUNCT_DIVISION_DATES,
        DAY_STOP,
        PUNCT.optional(),
        or_(
            MONTH_NAME_STOP,
            MONTH_STOP,
            MONTH_LATIN_NAME_STOP
        ),
        PUNCT.optional(),
        or_(
            YEAR_STOP,
            YEAR_SHORT_STOP
        ),
        YEAR_WORD.optional()
    ),
    # 1/I-1900 - 2/II-1901
    rule(
        DAY_START,
        PUNCT,
        MONTH_LATIN_NAME_START,
        '-',
        or_(
            YEAR_START,
            YEAR_SHORT_START
        ),
        PUNCT_DIVISION_DATES,
        DAY_STOP,
        PUNCT,
        MONTH_LATIN_NAME_STOP,
        '-',
        or_(
            YEAR_STOP,
            YEAR_SHORT_STOP
        ),
        YEAR_WORD.optional()
    ),
    # 1.1.1900 / 1/II/1900 / 1 января
    rule(
        DAY_START,
        PUNCT.optional(),
        or_(
            MONTH_START,
            MONTH_NAME_START,
            MONTH_LATIN_NAME_START
        ),
        PUNCT.optional(),
        or_(
            YEAR_START,
            YEAR_SHORT_START
        ).optional(),
        YEAR_WORD.optional()
    ),
    # 1/II-1900
    rule(
        DAY_START,
        PUNCT,
        MONTH_LATIN_NAME_START,
        '-',
        or_(
            YEAR_START,
            YEAR_SHORT_START
        ),
        YEAR_WORD.optional()
    ),
    # 1900 год
    rule(
        YEAR_START,
        YEAR_WORD.optional()
    ),
    # январь 1900 года
    rule(
        MONTH_NAME_START,
        or_(
            YEAR_START,
            YEAR_SHORT_START
        ),
        YEAR_WORD.optional()
    ),
).interpretation(
    DateRange
)


def date_extractor_for_diary(text):
    res = {
        'date_start' : [],
        'date_stop' : [],
        'text' : []
    }
    entry = ''
    for paragraph in text.split('\n'):
        parser = Parser(DATE_RANGE)
        for match in parser.findall(paragraph):
            record = match.fact.normalized
            if record.spans[0].start in range (0, 3):
                start = record.get_start_date
                stop = record.get_stop_date
                res['date_start'].append(start)
                res['date_stop'].append(stop)
                if entry != '':
                    res['text'].append(entry)
                    entry = ''
                break
        entry += paragraph
        entry += '\n'
    if entry != '':
        res['text'].append(entry)
    
    return pd.DataFrame(res)

def normalize_dates(start, stop):
    if start == stop:
        return start
    else: 
        return f'{start} - {stop}'

######## USAGE ###########

# parser = Parser(DATE_RANGE)

# text = '''
# 1943

# 24 марта. Челябинск

# Сегодня кончается третья четверть. Потом каникулы до 1/IV — неделю. Говорили с Москвой. Папка может предет в апреле. Хорошо бы приехал.
# Я немного болел. Теперь выздоровел. От класса отстал не намного. За каникулы догоню. Во дворе у нас несколько ребят уехало. Г.Л. обещала написать письмо. Посмотрим.
# Сегодня мне сообщили что И[нна].Д[митриева]. в меня втрескалась[.] Чтоб ей лопнуть! Неужели без любви нельзя обойтись. У наших ребят какое-то странное понимание о дружбе. Если увидят что стоишь и разговариваешь с какой-нибудь девочкой. Сразу дразнить: влюбился, влюбился. А для того что-бы влюбиться по моему надо подрасти. А у нас во дворе нет таких что-бы не перелюбились. В половине этого случая не исключая и меня.
# В школе то-же. Какие-то идиоты кругом. Как дикари. Ну, а я то-же не лучше. Я могу влюбиться сердцем, умом никогда.

# 25 марта. «И в какой стороне я не буду по какой не пройду я тропе, друга я никогда незабуду если с ним подружился в Москве…» 
# Друга хорошего нельзя позыбыть не только если с ним подружишь в Москве.
# «В какой точке Союза не буду, и где не встречу мой друг я тебя, я тебя никогда не забуду, если ты не забудешь меня».
# «Я сейчас сижу в тюрьме и не светит
# Солнце мне, Кашмари, кашмари, кашмари[»].
# Эх! Не знаю что у меня на душе, что в животе я знаю там глисты, сегодня получил анализ кала.
# Чорт меня побрал! Что это на меня нашло такое настроение влюбленного. Ну, ка пошлю вон. Быть тебе только другом но…
# Опять!?
# Последнее время я не знаю что со мной творится, но примерно догадываюсь, [запись обрывается]

# 5 апреля. Началась последняя четверть. А там испытания. Кончу 6-й кл[асс]. наверно в Челябинске. В апреле в Москву конечно не поедем.
# В выходной ходил стрелять в тир. Сдал на «Юный ворошиловский стрелок» .
# Книга — лучший друг мой. Но такие книги что я читаю не могут заменить друга — человека. Друг. Как это слово звучит для меня непривычно. О нем я могу лишь мечтать. Дружба. Я так нуждаюсь в тебе.

# 26/VIII-38 г. Весь день приготовления. Завтра едем совсем в Гдов. Вообще весь день шаталась из угла в угол, но ничего хорошего не сделала. Кой-чего выстирала. Читала. Много брусники ела. Вечером были в бане с Валей Павловой в нашей. Идем в баню, а на реке Беляев, Ванька дядин Мишкин, потом пришел Петька. Долго с ними ругались, но они ушли и мы вымылись. К школе не пошла. Весь вечер читала. Слышу, пошли от школы. Беляев остановился над окном и кричит — Марготя!
# Я нисколько не изменила своего положения, только чуть улыбнулась. Он больше ничего не сказал. Я после читала очень долго. Вообще, я сказала, что сегодня спать не буду. Немного пописала дневник, но спать все же захотелось. Легла, а Ляля сидит. Велела ей разбудить как будет ложиться.

# 27/VIII-38 г. Через час как раз она пошла спать. Я встала. Опять читала. Валя начала плакать. С ней долго возилась. Начинает светлеть. Уже три. Еще в первом часу у меня были Валя Павлова с Тоней Ефремовой — она сегодня ночует у Вали и с нами вместе едет. Сговорились в четыре ехать. Разбудила маму. Быстро собрались, поехали. Павловы проспали, даже и тетя Настя. Ну поехали. До свиданье Заовражье! Сегодня все наши едут в Ленинград. За Рудном я захотела спать и легла, но спала не много, а только лежала. В Вейне остановились, по кушали немного. Конфет 300 гр. взяла. Поехали дальше. Всю дорогу хохотали. Ну Ефремова — это черт! Так и смешит. На поезд опоздали. За железной дорогой, не доезжая еще деревни Добручи, опять кормили лошадь и сами обедали. Я очень замаялась и спать хочу, но надо размаяться. За Добручи заехали, стало веселее. Дорога прямая. Только и отсчитываем верстовые столбы.

# 17 сентября (четверг), 1970 год

# 18 сентября (пятница), 1970 год

# Юрка, Юрка, ты не сдерживаешь свое слово

# 1-12.1. Рло

# 1/I - 2/II лоиывал
# '''

# for match in parser.findall(text):
#     record = match.fact.normalized
#     # print(record.spans)
#     start = record.get_start_date
#     stop = record.get_stop_date
#     if start != stop:
#         print(f'{start} - {stop}')
#     else:
#         print(start)