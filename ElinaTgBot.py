#!/usr/bin/python3.11
import telebot
from telebot import types
import json
import os

bot = telebot.TeleBot('7937756954:AAFXwqLKMSiYZCtg7LPcjMgtYcahGiOWcx4');

PASSWORD = '02.11.2003'

user_authenticated = {}
gift_reservations = {}
surprise_reservations = set()
data_file = 'gift_data.json'

# Инициализация данных
gifts = {
    "Беспроводная зарядная станция": False,
    "Сертификат на мастер-класс": False,
    "Память для PC": False,
    "Джостик": False,
    "Зеленое растение в горшке": False,
    "Большая чашка для чая": False,
    "Шарм для браслета": False,
    "Робберт Паттинсон": False,
}

surprise_gift = {
    "Подарок сюрприз": 0,
}

# Функция для загрузки данных из файла
def load_data():
    global gift_reservations, gifts, surprise_gift
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            data = json.load(file)
            gift_reservations = data.get("gift_reservations", {})
            gifts.update(data.get("gifts", {}))
            surprise_gift.update(data.get("surprise_gift", {}))

# Функция для сохранения данных в файл
def save_data():
    data = {
        "gift_reservations": gift_reservations,
        "gifts": gifts,
        "surprise_gift": surprise_gift
    }
    with open(data_file, 'w') as file:
        json.dump(data, file)

# Загрузка данных при запуске
load_data()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_authenticated[user_id] = False
    bot.send_message(user_id, "🎉 Привет! Я — твой помощник на Секретной вечеринке Элины! 🎉 Чтобы войти, пожалуйста, введи пароль (подсказка - ХХ.ХХ.ХХХХ):")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_id = message.from_user.id

    if user_id not in user_authenticated:
        user_authenticated[user_id] = False

    # Проверка пароля
    if not user_authenticated[user_id]:
        if message.text == PASSWORD:
            user_authenticated[user_id] = True
            bot.send_message(user_id, "✅ Пароль принят! Теперь у нас есть доступ к самым важным деталям праздника.")
            show_main_menu(user_id)
        else:
            bot.send_message(user_id, "❌ Неправильный пароль. Попробуй снова.")
        return

    # Если пользователь аутентифицирован
    if message.text == '📍 Обязательно к прочтению':
        bot.send_message(user_id, 
                        "✨ Предыстория к квесту:\n"
                        "Вы — группа друзей, которая безумно фанатеет от любых упоминаний паранормальной активности. Вы уже давно изучаете эту тему, следите за новостями и различными сверхъестественными проявлениями. И вот вы решили, что хотите опробовать это на себе и навсегда развеять свои сомнения и страхи. Вы записываетесь на сеанс к экстрасенсу Элис, которая по вашим данным может погрузить вас в астрал.\n\n"
                        "⚠️ Важно:\n"
                        "Не опаздывай! Встречаемся в 17:20 на станции м.Нарвская или в 17:40 уже по адресу ул. Лифляндская 3.\n\n"
                        "🚨 ВНИМАНИЕ: В квесте присутствует задымление игрового пространства с безвредным для здоровья дымом. Участники с астмой до игры не допускаются. Также людям с эпилепсией участие запрещено.\n")

    elif message.text == '⏰ Время и место':
        bot.send_message(user_id, 
                        "🕒 Время встречи:\n"
                        "Мы встречаемся 2 ноября в 17:20 на станции м.Нарвская или в 17:40 уже по адресу.\n\n"
                        "📍 Место встречи:\n"
                        "Адрес: ул. Лифляндская 3.\n\n"
                        "🎥 Видео как добраться до квеста(фиксик поломал разрешение😗)\n")
        with open('wayToQuest.MP4', 'rb') as video_file:
            bot.send_video(user_id, video_file)
        
    elif message.text == '🎁 Вишлист':
        show_gift_list(user_id)

    elif message.text == '💅 Дресскод':
        bot.send_message(user_id, 
                        "Его нет!!! Одевайся так, как тебе удобно) \nP.s. Ты всегда выглядишь на 100 из 100💕")

    else:
        handle_gift_selection(message)

def show_gift_list(user_id):
    gifts_list = "\n".join([f"{gift} - {'❌' if status else '✅'}" for gift, status in gifts.items()])
    gifts_list += f"\n\nПодарок сюрприз - выбрали: {surprise_gift['Подарок сюрприз']} человек"
    bot.send_message(user_id, f"🎁 Вот несколько идей для подарков! Если у тебя уже есть свой вариант — смело дари его!\n\n{gifts_list}\n\nВведите название подарка, чтобы его занять или освободить.\n\n ✅ - подарок свободен \n ❌ - подарок занят")

@bot.message_handler(content_types=['text'])
def handle_gift_selection(message):
    user_id = message.from_user.id
    gift_name = message.text

    if gift_name in gifts:
        if gifts[gift_name]:  # Если подарок уже занят
            if gift_reservations.get(gift_name) == user_id:  # Проверка, забронировал ли этот пользователь
                gifts[gift_name] = False
                del gift_reservations[gift_name]
                bot.send_message(user_id, f"Вы отказались от подарка '{gift_name}'. Теперь он доступен для других.")
                save_data() 
            else:
                bot.send_message(user_id, "❌ Этот подарок уже занят другим пользователем.")
        else:  # Если подарок свободен
            gifts[gift_name] = True
            gift_reservations[gift_name] = user_id
            bot.send_message(user_id, f"Вы заняли подарок '{gift_name}'.")
            save_data()  

    elif gift_name == "Подарок сюрприз":
        if user_id in surprise_reservations:
            surprise_reservations.remove(user_id)
            surprise_gift["Подарок сюрприз"] -= 1
            bot.send_message(user_id, "Вы отказались от подарка Подарок сюрприз.")
        else:
            surprise_reservations.add(user_id)
            surprise_gift["Подарок сюрприз"] += 1
            bot.send_message(user_id, "Вы заняли Подарок сюрприз!")
        save_data()  

    else:
        bot.send_message(user_id, "Этот подарок не найден в списке. Пожалуйста, проверьте написание.")

def show_main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📍 Обязательно к прочтению')
    btn2 = types.KeyboardButton('⏰ Время и место')
    btn3 = types.KeyboardButton('🎁 Вишлист')
    btn4 = types.KeyboardButton('💅 Дресскод')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(user_id, "Выберите один из вариантов:", reply_markup=markup)

bot.polling(none_stop=True, interval=0)
