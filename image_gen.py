from PIL import Image, ImageDraw, ImageFont
import os

def create_life_card(life_data):
    # Создаем пустое изображение 800x600
    img = Image.new('RGB', (800, 600), color=(30, 30, 40))
    draw = ImageDraw.Draw(img)

    # Пытаемся загрузить шрифт (стандартный для Windows)
    try:
        font_large = ImageFont.truetype("arial.ttf", 45)
        font_med = ImageFont.truetype("arial.ttf", 30)
        font_small = ImageFont.truetype("arial.ttf", 22)
    except IOError:
        font_large = ImageFont.load_default()
        font_med = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Цвета
    white = (255, 255, 255)
    gray = (180, 180, 180)
    green = (100, 255, 100)
    red = (255, 100, 100)
    blue = (100, 200, 255)

    # Заголовок
    draw.text((400, 40), "Жизнь прожита", fill=white, font=font_large, anchor="mm")

    # Имя и Возраст
    status = f"{life_data['age']} лет" if life_data['alive'] else f"Умер(ла) в {life_data['age']} лет"
    draw.text((400, 110), f"{life_data['name']} — {status}", fill=gray, font=font_med, anchor="mm")
    
    if not life_data['alive']:
        draw.text((400, 150), f"Причина: {life_data['death_cause']}", fill=red, font=font_small, anchor="mm")

    # Левая колонка
    draw.text((50, 200), "🌍 Место рождения:", fill=gray, font=font_small)
    draw.text((50, 230), f"{life_data['country']} ({life_data['town']})", fill=white, font=font_med)

    draw.text((50, 290), "👤 Пол и Семья:", fill=gray, font=font_small)
    draw.text((50, 320), f"{life_data['gender']}, {life_data['family']} семья", fill=white, font=font_med)

    draw.text((50, 380), "🎓 Образование:", fill=gray, font=font_small)
    draw.text((50, 410), f"{life_data['education']}", fill=white, font=font_med)

    draw.text((50, 470), "💼 Работа:", fill=gray, font=font_small)
    draw.text((50, 500), f"{life_data['job']}", fill=white, font=font_med)

    # Правая колонка
    draw.text((450, 200), "❤️ Здоровье:", fill=gray, font=font_small)
    draw.text((450, 230), f"{int(life_data['health'])}", fill=green if life_data['health'] > 50 else red, font=font_med)

    draw.text((450, 290), "😊 Счастье:", fill=gray, font=font_small)
    draw.text((450, 320), f"{int(life_data['happiness'])}", fill=green if life_data['happiness'] > 50 else red, font=font_med)

    draw.text((450, 380), "🤝 Отношения:", fill=gray, font=font_small)
    draw.text((450, 410), f"Партнёр: {'да' if life_data['partner'] else 'нет'} | Дети: {life_data['children']}", fill=white, font=font_med)

    draw.text((450, 470), "💰 Доход:", fill=gray, font=font_small)
    draw.text((450, 500), f"{life_data['income']} $/год", fill=blue, font=font_med)

    # Рамка
    draw.rectangle([10, 10, 790, 590], outline=gray, width=3)

    # Сохраняем
    filepath = "life_card.png"
    img.save(filepath)
    return filepath