COUNTRIES = [
    {"code":"IN","name":"Индия","birth_share":0.176,"life_m":72.0,"life_f":76.3,"gdp":8500,"edu":0.55,"urban":0.36},
    {"code":"CN","name":"Китай","birth_share":0.067,"life_m":77.9,"life_f":82.5,"gdp":23000,"edu":0.70,"urban":0.65},
    {"code":"NG","name":"Нигерия","birth_share":0.057,"life_m":54.5,"life_f":58.4,"gdp":5500,"edu":0.40,"urban":0.54},
    {"code":"PK","name":"Пакистан","birth_share":0.052,"life_m":67.6,"life_f":70.7,"gdp":6500,"edu":0.40,"urban":0.37},
    {"code":"ID","name":"Индонезия","birth_share":0.034,"life_m":71.1,"life_f":75.3,"gdp":14000,"edu":0.60,"urban":0.58},
    {"code":"CD","name":"ДР Конго","birth_share":0.033,"life_m":61.9,"life_f":64.7,"gdp":1500,"edu":0.35,"urban":0.47},
    {"code":"ET","name":"Эфиопия","birth_share":0.031,"life_m":65.0,"life_f":68.0,"gdp":3000,"edu":0.35,"urban":0.23},
    {"code":"US","name":"США","birth_share":0.028,"life_m":75.0,"life_f":80.5,"gdp":76000,"edu":0.88,"urban":0.83},
    {"code":"BD","name":"Бангладеш","birth_share":0.026,"life_m":72.0,"life_f":74.5,"gdp":8000,"edu":0.50,"urban":0.40},
    {"code":"BR","name":"Бразилия","birth_share":0.024,"life_m":72.0,"life_f":79.0,"gdp":18000,"edu":0.65,"urban":0.87},
    {"code":"RU","name":"Россия","birth_share":0.017,"life_m":68.0,"life_f":78.0,"gdp":32000,"edu":0.80,"urban":0.75},
    {"code":"MX","name":"Мексика","birth_share":0.016,"life_m":72.0,"life_f":77.5,"gdp":22000,"edu":0.65,"urban":0.81},
    {"code":"JP","name":"Япония","birth_share":0.011,"life_m":81.0,"life_f":87.0,"gdp":45000,"edu":0.90,"urban":0.92},
    {"code":"PH","name":"Филиппины","birth_share":0.020,"life_m":68.0,"life_f":74.0,"gdp":9000,"edu":0.60,"urban":0.48},
    {"code":"EG","name":"Египет","birth_share":0.019,"life_m":68.0,"life_f":73.0,"gdp":13000,"edu":0.55,"urban":0.43},
    {"code":"VN","name":"Вьетнам","birth_share":0.015,"life_m":71.0,"life_f":78.0,"gdp":12000,"edu":0.65,"urban":0.40},
    {"code":"DE","name":"Германия","birth_share":0.010,"life_m":78.5,"life_f":83.5,"gdp":55000,"edu":0.90,"urban":0.78},
    {"code":"GB","name":"Великобритания","birth_share":0.009,"life_m":78.5,"life_f":82.5,"gdp":50000,"edu":0.90,"urban":0.84},
    {"code":"TR","name":"Турция","birth_share":0.015,"life_m":74.0,"life_f":79.0,"gdp":30000,"edu":0.70,"urban":0.77},
    {"code":"IR","name":"Иран","birth_share":0.018,"life_m":72.0,"life_f":76.0,"gdp":15000,"edu":0.65,"urban":0.76},
    {"code":"TH","name":"Таиланд","birth_share":0.009,"life_m":73.0,"life_f":80.0,"gdp":18000,"edu":0.70,"urban":0.52},
    {"code":"TZ","name":"Танзания","birth_share":0.028,"life_m":63.0,"life_f":67.0,"gdp":2800,"edu":0.35,"urban":0.37},
    {"code":"ZA","name":"ЮАР","birth_share":0.012,"life_m":60.0,"life_f":67.0,"gdp":13000,"edu":0.65,"urban":0.67},
    {"code":"KE","name":"Кения","birth_share":0.015,"life_m":62.0,"life_f":67.0,"gdp":4500,"edu":0.50,"urban":0.28},
    {"code":"KR","name":"Южная Корея","birth_share":0.004,"life_m":80.5,"life_f":86.5,"gdp":45000,"edu":0.90,"urban":0.81},
    {"code":"ES","name":"Испания","birth_share":0.004,"life_m":80.0,"life_f":85.5,"gdp":40000,"edu":0.85,"urban":0.81},
    {"code":"AR","name":"Аргентина","birth_share":0.007,"life_m":73.0,"life_f":79.0,"gdp":22000,"edu":0.75,"urban":0.92},
    {"code":"UA","name":"Украина","birth_share":0.004,"life_m":66.0,"life_f":76.0,"gdp":12000,"edu":0.80,"urban":0.70},
    {"code":"DZ","name":"Алжир","birth_share":0.009,"life_m":74.0,"life_f":78.0,"gdp":13000,"edu":0.60,"urban":0.74},
    {"code":"MA","name":"Марокко","birth_share":0.007,"life_m":72.0,"life_f":76.0,"gdp":8000,"edu":0.55,"urban":0.64},
    {"code":"OTHER","name":"Другие страны","birth_share":0.349,"life_m":70.0,"life_f":75.0,"gdp":15000,"edu":0.60,"urban":0.55},
]

CAUSES_YOUNG = ["инфекция", "авария", "врождённое заболевание", "пневмония"]
CAUSES_ADULT = ["болезнь сердца", "рак", "авария", "инсульт", "осложнение хронической болезни", "самоубийство", "убийство"]
CAUSES_OLD   = ["болезнь сердца", "рак", "пневмония", "старость", "инсульт", "болезнь Альцгеймера"]

EVENTS_CHILD = [
    "Нашёл новых друзей", "Заболел простудой", "Победил в школьном конкурсе", 
    "Попал в небольшую аварию", "Родители купили велосипед", "Получил двойку", 
    "Выиграл школьную олимпиаду", "Сломал руку", "Нашёл бездомного котёнка"
]
EVENTS_ADULT = [
    "Получил повышение", "Потерял работу", "Встретил важного человека", 
    "Заболел", "Выиграл небольшую сумму в лотерею", "Попал в ДТП", 
    "Нашёл хобби", "Встретил старую любовь", "Съездил в отпуск", 
    "Купил машину", "Взял ипотеку", "Поругался с другом"
]
EVENTS_OLD = [
    "Вышел на пенсию", "Заболел", "Стал дедушкой/бабушкой", 
    "Потерял друга", "Путешествие", "Нашёл новый смысл жизни", 
    "Написал мемуары", "Завёл собаку"
]
