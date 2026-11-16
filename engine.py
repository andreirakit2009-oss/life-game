import random
from dataclasses import dataclass, field, asdict
from data import COUNTRIES, CAUSES_YOUNG, CAUSES_ADULT, CAUSES_OLD, EVENTS_CHILD, EVENTS_ADULT, EVENTS_OLD

@dataclass
class Life:
    name: str
    country: str = ""
    gender: str = "мужской"
    family: str = "средняя"
    town: str = "город"
    health: int = 80
    happiness: int = 60
    knowledge: int = 10
    relations: int = 60
    income: int = 0
    age: int = 0
    alive: bool = True
    partner: bool = False
    children: int = 0
    education: str = "нет"
    job: str = "нет"
    log: list = field(default_factory=list)
    pending_choice: str | None = None
    pending_options: list = field(default_factory=list)
    death_cause: str | None = None
    country_data: dict = field(default_factory=dict)

    def add(self, text):
        self.log.append(f"{self.age} лет: {text}")

def random_country():
    r = random.random(); acc = 0
    for c in COUNTRIES:
        acc += c["birth_share"]
        if r <= acc: return c
    return COUNTRIES[-1]

def birth(name: str) -> Life:
    c = random_country()
    gender = random.choice(["мужской","женский"])
    family = random.choices(["бедная","средняя","обеспеченная"], weights=[0.4,0.45,0.15])[0]
    town = random.choices(["город","село"], weights=[c["urban"],1-c["urban"]])[0]
    life = Life(name=name, country=c["name"], gender=gender, family=family,
                town=town, health=random.randint(65,95), country_data=c)
    life.income = int(c["gdp"] * {"бедная":0.2,"средняя":0.5,"обеспеченная":1.2}[family] / 10)
    life.add(f"Родились {'мальчиком' if gender=='мужской' else 'девочкой'} в {family} семье, {town} — {c['name']}.")
    _schedule(life)
    return life

def _schedule(life: Life):
    choices = {
        6:  ("Учёба", ["Усердно учиться","Больше играть","Помогать семье"]),
        17: ("После школы", ["Университет","Работа","Колледж/ремесло"]),
        22: ("Работа", ["Искать хорошую работу","Начать своё дело","Продолжить учёбу"]),
        25: ("Отношения", ["Искать любовь","Сосредоточиться на карьере","Путешествовать"]),
        30: ("Семья", ["Завести детей","Не заводить детей","Усыновить"]),
        45: ("Кризис среднего возраста", ["Сменить профессию","Инвестировать в здоровье","Больше времени с семьёй"]),
        60: ("Переезд", ["Остаться","Переехать в другую страну","Переехать в город/село"]),
    }
    if life.age in choices:
        life.pending_choice, life.pending_options = choices[life.age]

def step(life: Life):
    if not life.alive: return "Жизнь уже завершена."
    life.age += 1
    events = []
    decay = 0.3 if life.age < 40 else 0.8 if life.age < 65 else 1.8
    life.health = max(0, min(100, life.health - decay + random.uniform(-1.5,1.5)))
    if 6 <= life.age <= 22 and life.education != "высшее":
        life.knowledge = min(100, life.knowledge + random.uniform(1,4))
    if life.age >= 18 and life.job != "нет":
        life.income = int(life.income * random.uniform(0.95,1.08) + random.randint(100,3000))
    if life.partner or life.children:
        life.relations = min(100, life.relations + random.uniform(0,2))
    life.happiness = int(0.6*life.happiness + 0.2*life.health + 0.1*life.relations + 0.1*min(100, life.income/1000))
    
    if random.random() < 0.15:
        events.append(_random_event(life))
        
    if _dies(life):
        life.alive = False
        life.death_cause = _cause(life)
        life.add(f"Жизнь закончилась в {life.age} лет. Причина: {life.death_cause}.")
        events.append(f"💀 Жизнь закончилась в {life.age} лет. Причина: {life.death_cause}.")
    else:
        _schedule(life)
    return " ".join(events) if events else ""

def _dies(life: Life) -> bool:
    c = life.country_data or COUNTRIES[0]
    le = c["life_f"] if life.gender == "женский" else c["life_m"]
    p = 1 / max(1, (le - life.age)) if life.age < le else 0.25
    p *= (1.5 - life.health/100)
    if life.income < 2000: p *= 1.3
    if life.age <= 1: p *= 2.5
    return random.random() < p

def _cause(life: Life) -> str:
    pool = CAUSES_YOUNG if life.age < 5 else CAUSES_ADULT if life.age < 60 else CAUSES_OLD
    return random.choice(pool)

def _random_event(life: Life) -> str:
    if life.age < 18:
        pool = EVENTS_CHILD
    elif life.age < 60:
        pool = EVENTS_ADULT
    else:
        pool = EVENTS_OLD
        
    ev = random.choice(pool)
    if "Заболел" in ev: life.health -= random.randint(3,15)
    if "Повышение" in ev: life.income += random.randint(1000,5000); life.happiness += 5
    if "Потерял работу" in ev: life.income = max(0, life.income//2); life.happiness -= 8
    if "Выиграл" in ev: life.income += 500; life.happiness += 10
    if "ДТП" in ev or "аварию" in ev: life.health -= 20
    life.add(ev)
    return ev

def apply_choice(life: Life, idx: int) -> str:
    if not life.pending_choice: return "Сейчас нет развилки."
    option = life.pending_options[idx]
    life.add(f"Выбор: {option}")
    ch = life.pending_choice
    if ch == "Учёба":
        if option == "Усердно учиться": life.knowledge += 15; life.happiness -= 3
        elif option == "Больше играть": life.happiness += 8; life.relations += 5
        else: life.relations += 8; life.income += 100
    elif ch == "После школы":
        if option == "Университет": life.education = "высшее"; life.knowledge += 20
        elif option == "Работа": life.job = "рабочий"; life.income += 2000
        else: life.education = "колледж"; life.job = "специалист"; life.income += 1500
    elif ch == "Работа":
        if option == "Искать хорошую работу":
            life.job = random.choice(["инженер","учитель","врач","менеджер"]); life.income += 5000
        elif option == "Начать своё дело":
            life.job = "предприниматель"; life.income += 8000; life.happiness += 5
        else: life.education = "магистр"; life.knowledge += 10
    elif ch == "Отношения":
        if option == "Искать любовь": life.partner = random.random() < 0.7; life.happiness += 10
        elif option == "Сосредоточиться на карьере": life.income += 3000; life.happiness -= 3
        else: life.happiness += 12
    elif ch == "Семья":
        if option == "Завести детей": life.children += random.randint(1,3); life.happiness += 5
        elif option == "Не заводить детей": life.happiness += 3
        else: life.children += 1; life.happiness += 8
    elif ch == "Кризис среднего возраста":
        if option == "Сменить профессию":
            life.job = random.choice(["фермер","программист","писатель","ремесленник"])
            life.income = int(life.income*1.2); life.happiness += 5
        elif option == "Инвестировать в здоровье": life.health = min(100, life.health+15)
        else: life.relations += 10; life.happiness += 8
    elif ch == "Переезд":
        if option == "Переехать в другую страну":
            c = random.choice([x for x in COUNTRIES if x["code"] != "OTHER"])
            life.country_data = c; life.country = c["name"]
            life.income = int(life.income*1.5); life.happiness += 5
        elif option == "Переехать в город/село":
            life.town = "село" if life.town == "город" else "город"
    life.pending_choice = None
    life.pending_options = []
    return f"Вы выбрали: {option}"

def card(life: Life) -> str:
    status = "жив" if life.alive else f"умер в {life.age} лет ({life.death_cause})"
    return (f"👤 {life.name}\n"
            f"Страна: {life.country} ({life.town})\n"
            f"Пол: {life.gender} · Семья: {life.family}\n"
            f"Возраст: {life.age} · {status}\n"
            f"Образование: {life.education} · Работа: {life.job}\n"
            f"Партнёр: {'да' if life.partner else 'нет'} · Дети: {life.children}\n"
            f"❤️ Здоровье {int(life.health)} · 😊 Счастье {int(life.happiness)}\n"
            f"📚 Знания {int(life.knowledge)} · 🤝 Отношения {int(life.relations)}\n"
            f"💰 Доход: {life.income} $/год")