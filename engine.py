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
    money: int = 0        
    expenses: int = 0     
    debt: int = 0         
    age: int = 0
    alive: bool = True
    
    # Семья
    partner: bool = False
    partner_name: str = ""
    children: int = 0
    grandchildren: int = 0
    divorced: bool = False
    
    education: str = "нет"
    job: str = "нет"
    log: list = field(default_factory=list)
    pending_choice: str | None = None
    pending_options: list = field(default_factory=list)
    death_cause: str | None = None
    country_data: dict = field(default_factory=dict)
    focus: str = "Баланс"

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
    family = random.choices(["бедная","средняя","обеспеченная"], weights=[0.5,0.35,0.15])[0]
    town = random.choices(["город","село"], weights=[c["urban"],1-c["urban"]])[0]
    
    base_health = random.randint(60, 90) + (15 if c["gdp"] > 30000 else 0) - (15 if c["gdp"] < 5000 else 0)
    
    life = Life(name=name, country=c["name"], gender=gender, family=family,
                town=town, health=max(20, min(100, base_health)), country_data=c, income=0, money=0)
    life.add(f"Родились {'мальчиком' if gender=='мужской' else 'девочкой'} в {family} семье, {town} — {c['name']}.")
    _schedule(life)
    return life

def _schedule(life: Life):
    if life.age == 6: 
        life.pending_choice, life.pending_options = "Школа", ["Усердно учиться","Больше играть","Помогать семье"]
    elif life.age == 14:
        life.pending_choice, life.pending_options = "Первые деньги", ["Начать подрабатывать", "Тратить время на учёбу", "Заниматься спортом"]
    elif life.age == 17: 
        life.pending_choice, life.pending_options = "После школы", ["Университет (платно)", "Университет (бюджет)", "Пойти работать", "Колледж"]
    elif life.age == 22: 
        life.pending_choice, life.pending_options = "Карьера", ["Искать стабильную работу", "Начать своё дело (нужен кредит)", "Продолжить учёбу"]
    
    # Брак в зависимости от страны
    marriage_age = 18 if life.country_data["gdp"] < 10000 else 22 if life.country_data["gdp"] < 30000 else 26
    
    if not life.partner and not life.divorced and life.age == marriage_age:
        life.pending_choice = "Брак"
        life.pending_options = ["Жениться/Выйти замуж", "Остаться одному/одной"]

    elif life.age == 30: 
        life.pending_choice, life.pending_options = "Семья", ["Завести детей", "Не заводить детей", "Усыновить"]
        
    elif life.age == 40: 
        life.pending_choice, life.pending_options = "Инвестиции", ["Инвестировать в бизнес", "Купить недвижимость", "Положить в банк"]
    elif life.age == 50: 
        life.pending_choice, life.pending_options = "Кризис", ["Сменить профессию", "Начать пить", "Уйти в религию", "Больше работать"]
    elif life.age == 60: 
        life.pending_choice, life.pending_options = "Пенсия", ["Выйти на пенсию", "Продолжать работать", "Переехать в деревню"]

def step(life: Life):
    if not life.alive: return "Жизнь уже завершена."
    life.age += 1
    events = []

    # Фокус
    if life.focus == "Здоровье": life.health = min(100, life.health + 2)
    elif life.focus == "Учёба" and 6 <= life.age <= 22: life.knowledge = min(100, life.knowledge + 3)
    elif life.focus == "Отношения": life.relations = min(100, life.relations + 2)

    # Здоровье
    decay = 0.3 if life.age < 40 else 0.8 if life.age < 65 else 1.8
    life.health = max(0, min(100, life.health - decay + random.uniform(-1.5,1.5)))

    # Доходы и расходы
    if life.job != "нет" and life.age >= 16:
        base_income = life.income if life.income > 0 else (life.country_data["gdp"] * 0.1)
        edu_mult = 1.5 if life.education == "высшее" else 1.2 if life.education == "колледж" else 1.0
        life.income = int(base_income * edu_mult + random.randint(100, 1000))
        
        if life.partner:
            life.income += int(life.country_data["gdp"] * 0.08)
            
        life.money += life.income
        
        base_expenses = life.country_data["gdp"] * 0.05
        if life.children > 0: base_expenses += 1000 * life.children
        if life.partner: base_expenses += 500
        if life.grandchildren > 0: base_expenses -= 500
        life.expenses = int(base_expenses)
        life.money -= life.expenses
        
        if life.debt > 0:
            payment = int(life.debt * 0.1)
            if life.money >= payment:
                life.money -= payment; life.debt -= payment
            else:
                life.debt += int(life.debt * 0.05); life.happiness -= 5
                
        if life.money < 0:
            life.debt += abs(life.money); life.money = 0
            life.health -= 5; life.happiness -= 10
            events.append("Жизнь в долг, стресс.")
    else:
        life.income = 0

    # Отношения и развод
    if life.partner:
        life.relations = min(100, life.relations + 1)
        divorce_chance = 0.02 if life.country_data["gdp"] > 30000 else 0.005
        if life.relations < 30 and random.random() < divorce_chance:
            life.partner = False; life.divorced = True
            life.money = int(life.money * 0.5)
            life.happiness -= 20
            events.append(f"Развод с {life.partner_name}. Потеряна половина денег.")

    # Внуки
    if life.children > 0 and 50 <= life.age <= 65 and life.grandchildren == 0:
        if random.random() < 0.3:
            grandchildren_count = 1 if life.country_data["gdp"] > 30000 else random.randint(1, 4)
            life.grandchildren += grandchildren_count
            life.happiness += 15
            life.health += 5
            events.append(f"Родились внуки! ({grandchildren_count} чел.)")

    life.happiness = int(0.6*life.happiness + 0.2*life.health + 0.1*life.relations + 0.1*min(100, life.money/1000))

    if random.random() < 0.20:
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
    if life.money < (c["gdp"] * 0.05): p *= 1.4
    if life.age <= 1: p *= 2.5
    return random.random() < p

def _cause(life: Life) -> str:
    pool = CAUSES_YOUNG if life.age < 5 else CAUSES_ADULT if life.age < 60 else CAUSES_OLD
    return random.choice(pool)

def _random_event(life: Life) -> str:
    if life.age < 18: pool = EVENTS_CHILD
    elif life.age < 60: pool = EVENTS_ADULT
    else: pool = EVENTS_OLD
    ev = random.choice(pool)
    if "Заболел" in ev: life.health -= random.randint(5,20); life.money -= 500
    if "Повышение" in ev: life.income += random.randint(1000,5000); life.happiness += 5
    if "Потерял работу" in ev: life.income = 0; life.job = "нет"; life.happiness -= 15
    if "Выиграл" in ev: life.money += 5000; life.happiness += 15
    if "ДТП" in ev or "аварию" in ev: life.health -= 30; life.money -= 2000
    life.add(ev)
    return ev

def apply_choice(life: Life, idx: int) -> str:
    if not life.pending_choice: return "Сейчас нет развилки."
    option = life.pending_options[idx]
    life.add(f"Выбор: {option}")
    ch = life.pending_choice
    
    if ch == "Школа":
        if option == "Усердно учиться": life.knowledge += 15
        elif option == "Больше играть": life.happiness += 8; life.relations += 5
        else: life.relations += 8
    elif ch == "Первые деньги":
        if option == "Начать подрабатывать": life.money += 500; life.knowledge -= 5
        elif option == "Тратить время на учёбу": life.knowledge += 10
        else: life.health += 10
    elif ch == "После школы":
        if option == "Университет (платно)": life.education = "высшее"; life.knowledge += 20; life.debt += 5000
        elif option == "Университет (бюджет)": life.education = "высшее"; life.knowledge += 20
        elif option == "Работа": life.job = "рабочий"; life.income = life.country_data["gdp"] * 0.05
        else: life.education = "колледж"; life.job = "специалист"; life.income = life.country_data["gdp"] * 0.08
    elif ch == "Карьера":
        if option == "Искать стабильную работу": life.job = "менеджер"; life.income = life.country_data["gdp"] * 0.15
        elif option == "Начать своё дело (нужен кредит)": life.job = "предприниматель"; life.debt += 10000; life.income = life.country_data["gdp"] * 0.2
        else: life.education = "магистр"; life.knowledge += 10
    elif ch == "Брак":
        if option == "Жениться/Выйти замуж":
            life.partner = True
            names = ["Анна", "Елена", "Мария", "Ольга", "Дмитрий", "Александр", "Сергей", "Иван"]
            life.partner_name = random.choice(names)
            life.happiness += 20
            life.log.append(f"Брак с {life.partner_name}.")
        else:
            life.happiness -= 5
    elif ch == "Семья":
        if option == "Завести детей": life.children += random.randint(1,3); life.happiness += 10
        elif option == "Не заводить детей": life.happiness += 3
        else: life.children += 1; life.happiness += 8
    elif ch == "Инвестиции":
        if option == "Инвестировать в бизнес":
            if random.random() > 0.5: life.money += 15000
            else: life.money -= 5000
        elif option == "Купить недвижимость": life.money -= 20000; life.happiness += 10
        else: life.money += int(life.money * 0.05)
    elif ch == "Кризис":
        if option == "Сменить профессию": life.job = "программист"; life.income = int(life.income*1.2)
        elif option == "Начать пить": life.health -= 20; life.happiness += 5
        elif option == "Уйти в религию": life.happiness += 15; life.relations += 10
        else: life.income += 3000; life.happiness -= 10
    elif ch == "Пенсия":
        if option == "Выйти на пенсию": life.job = "нет"; life.income = life.country_data["gdp"] * 0.02
        elif option == "Продолжать работать": life.income += 1000
        else: life.town = "село"; life.happiness += 10; life.health += 5
            
    life.pending_choice = None
    life.pending_options = []
    return f"Вы выбрали: {option}"

def card(life: Life) -> str:
    status = "жив" if life.alive else f"умер в {life.age} лет ({life.death_cause})"
    fin_status = f"💰 Баланс: {life.money} $"
    if life.debt > 0: fin_status += f" (Долг: {life.debt} $)"
    
    family_info = ""
    if life.partner: family_info += f"В браке с {life.partner_name}\n"
    if life.children > 0: family_info += f"Дети: {life.children}\n"
    if life.grandchildren > 0: family_info += f"Внуки: {life.grandchildren}\n"
    
    return (f"👤 {life.name}\n"
            f"Страна: {life.country} ({life.town})\n"
            f"Пол: {life.gender} · Семья: {life.family}\n"
            f"Возраст: {life.age} · {status}\n"
            f"Образование: {life.education} · Работа: {life.job}\n"
            f"{family_info}"
            f"❤️ Здоровье {int(life.health)} · 😊 Счастье {int(life.happiness)}\n"
            f"📚 Знания {int(life.knowledge)} · 🤝 Отношения {int(life.relations)}\n"
            f"{fin_status} · Доход: {life.income} $/год\n"
            f"🎯 Фокус: {life.focus}")
