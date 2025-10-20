import telebot
from telebot import types
import webbrowser
from telebot.types import InlineKeyboardButton
import requests
import json
import yt_dlp
import os
from dotenv import load_dotenv
from currency_converter import CurrencyConverter

# Загружаем переменные окружения ПЕРВЫМ делом
load_dotenv()

# Получаем ключи из .env
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
WEATHER_API = os.getenv('WEATHER_API')
EXCHANGE_API_KEY = os.getenv('EXCHANGE_API_KEY')

# Проверяем что ключи загружены
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле!")

# Инициализируем бота ПЕРЕД всеми декораторами
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Теперь импортируем остальные модули
from currency_converter import CurrencyConverter

user_states = {}

# Проверяем доступность API (опционально)
if EXCHANGE_API_KEY:
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD"
    response = requests.get(url)
    data = response.json()
#Блок команд со слешами(/),
@bot.message_handler(commands=['site', 'website', 'web'])
def site(message):
    webbrowser.open('https://ru.freepik.com')

@bot.message_handler(commands=['start', 'main', 'hello'])
def main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Каталог действий')
    markup.row(btn1)
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, этот бот предназначен для удобства работы', reply_markup=markup)
    bot.register_next_step_handler(message, click)



def click(message):
    if message.text == 'Каталог действий':
        bot.register_next_step_handler(message, click)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('🌐На сайт', url='https://google.com')
        btn2 = types.InlineKeyboardButton('🤖Chat-gpt', url='https://chat-gpt.org/chat')
        btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
        markup.row(btn1, btn2, btn3)
        btn4 = types.InlineKeyboardButton('🔆Погода', callback_data='weather')
        btn5 = types.InlineKeyboardButton('🧠 Нейросеть', callback_data='neural_network')# Новая кнопка
        btn6 = types.InlineKeyboardButton('💸Валюта', callback_data='money')
        markup.row(btn4, btn5, btn6)
        btn_music_search = types.InlineKeyboardButton('🔍 Поиск музыки', callback_data='music_search')  # Новая кнопка
        markup.add(btn_music_search)
        btn7 = types.InlineKeyboardButton('🎶Безмятежность.exe', callback_data='muzz')
        markup.add(btn7)
        btn8 = types.InlineKeyboardButton('🎶Fantasy Mixtape', callback_data='muz')
        markup.add(btn8)
        btn_cancel = types.InlineKeyboardButton("Завершить", callback_data="cancel_catalog")
        markup.add(btn_cancel)
        bot.reply_to(message, 'Каталог:', reply_markup=markup)


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Help-information</b>', parse_mode='html')

#Блок функции с командами без слешов
@bot.message_handler()
def info(message):
      if message.text.lower() == 'привет':
          bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}')
      elif message.text.lower() == 'id':
          bot.reply_to(message, f'ID: {message.from_user.id}')
      elif message.text.lower() == 'ghbdtn':
          bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}')
      elif message.text.lower() == 'владелец':
          bot.reply_to(message, f'@blessed000000:')
      elif message.text.lower() == 'сосал?':
          bot.reply_to(message, f'да')


@bot.message_handler(content_types=['photo', 'video', 'audio', 'voice'])
def get_photo(message):

    # кнопка возле самого сообщенийя

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2, btn3)
    bot.reply_to(message, 'Какое красивое фото', reply_markup=markup)



@bot.callback_query_handler(func=lambda callback: callback.data == 'return_to_catalog')
def return_to_catalog(callback):
    print("Обработчик return_to_catalog вызван")  # Логирование для отладки
    # Очищаем состояние пользователя
    if callback.message.chat.id in user_states:
        del user_states[callback.message.chat.id]

    # Возвращаем пользователя в главное меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Каталог действий')
    markup.row(btn1)
    bot.send_message(callback.message.chat.id, "Вы вернулись в главное меню.", reply_markup=markup)
    bot.register_next_step_handler(callback.message, click)
# декоратор который отбрабатывает callback
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id -1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'weather':
        handle_weather_callback(callback)
    elif callback.data == "cancel_weather":
        cancel_weather(callback)
    elif callback.data == 'money':
        handle_money_callback(callback)
    elif callback.data == 'music_search':
        handle_music_search(callback)
    elif callback.data == "cancel_music_search":
        cancel_music_search(callback)
    elif callback.data.startswith('convert_'):
        handle_currency_selection(callback)
    elif callback.data == 'next_currency':
        handle_money_callback(callback)
    elif callback.data == 'finish_conversion':
        finish_conversion(callback)
    elif callback.data == 'muzz':
        file1 = open('./skrip/Скриптонит - улыбка (2).mp3', 'rb')
        file2 = open('./skrip/Скриптонит - fast furious (2).mp3', 'rb')
        file3 = open('./skrip/Скриптонит, кухня - эсмеральда (2).mp3', 'rb')
        file4 = open('./skrip/Скриптонит, T-Fest - 1, 2 (2).mp3', 'rb')
        file5 = open('./skrip/Скриптонит - там где не ждали.mp3', 'rb')
        file6 = open('./skrip/Скриптонит - cold as ice.mp3', 'rb')
        file7 = open('./skrip/Скриптонит - 8ballin (2).mp3', 'rb')
        file8 = open('./skrip/Скриптонит - лошадка (2).mp3', 'rb')
        file9 = open('./skrip/Скриптонит - незачем болеть (2).mp3', 'rb')
        file10 = open('./skrip/Скриптонит - як 4 (2).mp3', 'rb')
        file11 = open('./skrip/Скриптонит - туман (2).mp3', 'rb')
        file12 = open('./skrip/Скриптонит,_TAYÖKA_ничего_не_сделаешь (2).mp3', 'rb')
        file13 = open('./skrip/Скриптонит - электричество (2).mp3', 'rb')
        file14 = open('./skrip/Скриптонит,_даена,_Miyagi_Эндшпиль_мегаполис (2).mp3', 'rb')
        file15 = open('./skrip/Скриптонит -  жди меня (2).mp3', 'rb')
        file16 = open('./skrip./https___images.genius.com_c17dcc4af7619fb61acd2b55f1729c00.999x999x1.png', 'rb')
        bot.send_photo(callback.message.chat.id, file16)
        bot.send_audio(callback.message.chat.id, file1)
        bot.send_audio(callback.message.chat.id, file2)
        bot.send_audio(callback.message.chat.id, file3)
        bot.send_audio(callback.message.chat.id, file4)
        bot.send_audio(callback.message.chat.id, file5)
        bot.send_audio(callback.message.chat.id, file6)
        bot.send_audio(callback.message.chat.id, file7)
        bot.send_audio(callback.message.chat.id, file8)
        bot.send_audio(callback.message.chat.id, file9)
        bot.send_audio(callback.message.chat.id, file10)
        bot.send_audio(callback.message.chat.id, file11)
        bot.send_audio(callback.message.chat.id, file12)
        bot.send_audio(callback.message.chat.id, file13)
        bot.send_audio(callback.message.chat.id, file14)
        bot.send_audio(callback.message.chat.id, file15)
    elif callback.data == 'muz':
        file1 = open('./skripF/https___images.genius.com_8b3ac1f13e79d3ed0fe4f99c82f33175.1000x1000x1.png', 'rb')
        file2 = open('./skripF/Скриптонит - Аванс.mp3', 'rb')
        file3 = open('./skripF/Скриптонит_qurt_Caro_Сумка_Remix_Remix.mp3', 'rb')
        file4 = open('./skripF/Скриптонит_Malcolm_Ku_Веселей_Remix_Remix.mp3', 'rb')
        file5 = open('./skripF/Скриптонит_LOVV66_Мне_похуй_Remix_Remix.mp3', 'rb')
        file6 = open('./skripF/Скриптонит_FRIENDLY_T_Некогда_мечтать.mp3', 'rb')
        file7 = open('./skripF/Скриптонит_blandee_M_Obnovylle_Remix_Remix.mp3', 'rb')
        file8 = open('./skripF/Скриптонит  Словетский - Легал.mp3', 'rb')
        file9 = open('./skripF/Скриптонит  НЕДРЫ - Как у звезды.mp3', 'rb')
        file10 = open('./skripF/Скриптонит  кухня - Прицел.mp3', 'rb')
        file11 = open('./skripF/Скриптонит  Крип-а-Крип - Бонг.mp3', 'rb')
        file12 = open('./skripF/Скриптонит  Ulukmanapo - До конца.mp3', 'rb')
        file13 = open('./skripF/Скриптонит  tsb - Не вывихни шею.mp3', 'rb')
        file14 = open('./skripF/Скриптонит  TAYKA - Ковры.mp3', 'rb')
        file15 = open('./skripF/Скриптонит  OG Buda - Зита и Гита.mp3', 'rb')
        file16 = open('./skripF/Скриптонит  Kali  Malc... - Ей нравится.mp3', 'rb')
        file17 = open('./skripF/Скриптонит  Kali - Tonight (Remix) (Remix).mp3', 'rb')
        file18 = open('./skripF/Скриптонит  GDO - Лухари.mp3', 'rb')
        file19 = open('./skripF/Скриптонит  BULLYWO - Чистый (Remix) (Remix).mp3', 'rb')
        file20 = open('./skripF/Скриптонит  Beni Milordo - Allo-Allo.mp3', 'rb')
        file21 = open('./skripF/Скриптонит - 223 (Solo Version) (So.mp3', 'rb')
        file22 = open('./skripF/Скриптонит - Холодно.mp3', 'rb')
        file23 = open('./skripF/Скриптонит - Тост.mp3', 'rb')
        file24 = open('./skripF/Скриптонит - Татухи.mp3', 'rb')
        file25 = open('./skripF/Скриптонит - Затяжка.mp3', 'rb')
        file26 = open('./skripF/Скриптонит - Жизнь не сахар (Solo V.mp3', 'rb')
        file27 = open('./skripF/Скриптонит - Гастроли.mp3', 'rb')
        file28 = open('./skripF/Скриптонит - Будьте здоровы (2023 R.mp3', 'rb')
        file29 = open('./skripF/Скриптонит - Bad Vision (Solo Versi.mp3', 'rb')
        bot.send_photo(callback.message.chat.id, file1)
        bot.send_audio(callback.message.chat.id, file2)
        bot.send_audio(callback.message.chat.id, file3)
        bot.send_audio(callback.message.chat.id, file4)
        bot.send_audio(callback.message.chat.id, file5)
        bot.send_audio(callback.message.chat.id, file6)
        bot.send_audio(callback.message.chat.id, file7)
        bot.send_audio(callback.message.chat.id, file8)
        bot.send_audio(callback.message.chat.id, file9)
        bot.send_audio(callback.message.chat.id, file10)
        bot.send_audio(callback.message.chat.id, file11)
        bot.send_audio(callback.message.chat.id, file12)
        bot.send_audio(callback.message.chat.id, file13)
        bot.send_audio(callback.message.chat.id, file14)
        bot.send_audio(callback.message.chat.id, file15)
        bot.send_audio(callback.message.chat.id, file16)
        bot.send_audio(callback.message.chat.id, file17)
        bot.send_audio(callback.message.chat.id, file18)
        bot.send_audio(callback.message.chat.id, file19)
        bot.send_audio(callback.message.chat.id, file20)
        bot.send_audio(callback.message.chat.id, file21)
        bot.send_audio(callback.message.chat.id, file22)
        bot.send_audio(callback.message.chat.id, file23)
        bot.send_audio(callback.message.chat.id, file24)
        bot.send_audio(callback.message.chat.id, file25)
        bot.send_audio(callback.message.chat.id, file26)
        bot.send_audio(callback.message.chat.id, file27)
        bot.send_audio(callback.message.chat.id, file28)
        bot.send_audio(callback.message.chat.id, file29)
    elif callback.data == "cancel_catalog":
        bot.send_message(callback.message.chat.id, "Каталог закрыт.")
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)


# Новая функция для поиска музыки
def handle_music_search(callback):
    user_states[callback.message.chat.id] = "music_search"
    markup = types.InlineKeyboardMarkup()
    btn_cancel = types.InlineKeyboardButton("Завершить поиск музыки", callback_data="cancel_music_search")
    markup.add(btn_cancel)
    bot.send_message(callback.message.chat.id,
                     "Введите название песни и исполнителя (например: 'Shape of You - Ed Sheeran'):",
                     reply_markup=markup)
    bot.register_next_step_handler(callback.message, process_music_search)


def process_music_search(message):
    if user_states.get(message.chat.id) != "music_search":
        return

    if not message.text or message.text.strip() == "":
        bot.reply_to(message, "❌ Пожалуйста, введите название песни.")
        bot.register_next_step_handler(message, process_music_search)
        return

    query = message.text.strip() + " official audio"

    # Уведомление о начале поиска
    bot.send_chat_action(message.chat.id, 'typing')

    try:
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={YOUTUBE_API_KEY}&maxResults=1"
        res = requests.get(search_url, timeout=10)

        if res.status_code != 200 or not res.json().get('items'):
            bot.reply_to(message, "❌ Трек не найден. Попробуйте другой запрос.")
            bot.register_next_step_handler(message, process_music_search)
            return

        video_id = res.json()['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Улучшенные настройки yt-dlp с увеличенными таймаутами
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'track.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'socket_timeout': 30,
            'retries': 10,
            'fragment_retries': 10,
            'extract_flat': False,
            'http_chunk_size': 10485760,  # 10MB chunks
        }

        # Уведомление о начале скачивания
        bot.send_chat_action(message.chat.id, 'upload_audio')
        msg = bot.reply_to(message, "⏬ Скачиваю трек...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Отправка аудио
        with open('track.mp3', 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file, title=message.text)

        # Удаляем временный файл
        if os.path.exists('track.mp3'):
            os.remove('track.mp3')

        # Удаляем сообщение о скачивании
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        error_msg = f"❌ Ошибка при скачивании: {str(e)}"
        print(f"Ошибка: {e}")  # Для отладки
        bot.reply_to(message, error_msg)

    # Предлагаем новый поиск
    markup = types.InlineKeyboardMarkup()
    btn_cancel = types.InlineKeyboardButton("❌ Завершить поиск", callback_data="cancel_music_search")
    markup.add(btn_cancel)

    bot.reply_to(message, "🎵 Введите следующий запрос или завершите поиск:", reply_markup=markup)
    bot.register_next_step_handler(message, process_music_search)


def cancel_music_search(callback):
    user_states.pop(callback.message.chat.id, None)
    bot.send_message(callback.message.chat.id, "Поиск музыки завершён.")
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Каталог действий')
    markup.row(btn1)
    bot.send_message(callback.message.chat.id, "Вы вернулись в главное меню.", reply_markup=markup)
    bot.register_next_step_handler(callback.message, click)
def handle_weather_callback(callback):
        # Устанавливаем состояние пользователя в "weather"
    user_states[callback.message.chat.id] = "weather"

        # Создаем клавиатуру с кнопкой "Завершить поиск погоды"
    markup = types.InlineKeyboardMarkup()
    btn_cancel = types.InlineKeyboardButton("Завершить поиск погоды", callback_data="cancel_weather")
    markup.add(btn_cancel)

        # Запрашиваем город
    bot.send_message(callback.message.chat.id, "Введите название города:", reply_markup=markup)

        # Регистрируем следующий шаг для обработки города
    bot.register_next_step_handler(callback.message, process_weather)
def process_weather(message):
    if user_states.get(message.chat.id) != "weather":
        return  # Если состояние не "weather", игнорируем сообщение

    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric')

    if res.status_code != 200:
        bot.reply_to(message, "Город не найден. Попробуйте ещё раз.")
        bot.register_next_step_handler(message, process_weather)
        return

    data = json.loads(res.text)
    temp = data["main"]["temp"]

        # Создаем клавиатуру с кнопкой "Завершить поиск погоды"
    markup = types.InlineKeyboardMarkup()
    btn_cancel = types.InlineKeyboardButton("Завершить поиск погоды", callback_data="cancel_weather")
    markup.add(btn_cancel)

        # Отправляем сообщение с погодой и кнопкой
    img = '☀️' if temp > 10.0 else '🌤' if temp > 0.0 else '🌥' if temp > -10.0 else '❄️'
    bot.reply_to(message, f'Сейчас погода: {temp} {img}', reply_markup=markup)

        # Регистрируем следующий шаг для обработки нового города
    bot.register_next_step_handler(message, process_weather)
def cancel_weather(callback):
        # Сбрасываем состояние пользователя
    user_states.pop(callback.message.chat.id, None)

        # Отправляем сообщение о завершении
    bot.send_message(callback.message.chat.id, "Поиск погоды завершён.")

        # Удаляем клавиатуру с кнопкой "Завершить поиск погоды"
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
        # Возвращаем пользователя в главное меню

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Каталог действий')
    markup.row(btn1)
    bot.send_message(callback.message.chat.id, "Вы вернулись в главное меню.", reply_markup=markup)
    bot.register_next_step_handler(callback.message, click)
def get_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data.get('result') == 'success':
        return data.get('conversion_rate')
    else:
        return None
def handle_money_callback(callback):
    user_states[callback.message.chat.id] = "money"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='convert_USD_EUR')
    btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='convert_EUR_USD')
    btn3 = types.InlineKeyboardButton('RUB/SOM', callback_data='convert_RUB_KGS')
    btn4 = types.InlineKeyboardButton('SOM/RUB', callback_data='convert_KGS_RUB')
    btn5 = types.InlineKeyboardButton('💰Другая валюта', callback_data='convert_else')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    btn_cancel = types.InlineKeyboardButton("📛Завершить конвертацию", callback_data="cancel_money")
    markup.add(btn_cancel)
    bot.send_message(callback.message.chat.id, "Выберите пару валют:", reply_markup=markup)
def handle_currency_selection(callback):
    if callback.data == 'convert_else':
        # Запрашиваем у пользователя ввод пары валют
        bot.send_message(callback.message.chat.id, "Введите пару валют в формате USD/EUR:")
        bot.register_next_step_handler(callback.message, process_custom_currency_pair)
    elif '_' in callback.data:
        currency_pair = callback.data.split('_')[1:]  # Получаем пару валют
        user_states[callback.message.chat.id] = {'currency_pair': currency_pair}
        bot.send_message(callback.message.chat.id, "Введите сумму для конвертации:")
        bot.register_next_step_handler(callback.message, process_amount)
    else:
        bot.send_message(callback.message.chat.id, "Ошибка: неверный формат валютной пары.")
def process_custom_currency_pair(message):
    try:
        # Разделяем введенную строку на две валюты
        base_currency, target_currency = message.text.strip().upper().split('/')
        user_states[message.chat.id] = {'currency_pair': [base_currency, target_currency]}
        bot.send_message(message.chat.id, "Введите сумму для конвертации:")
        bot.register_next_step_handler(message, process_amount)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Введите пару валют в формате USD/EUR.")
        bot.register_next_step_handler(message, process_custom_currency_pair)
# Обработчик ввода суммы
def process_amount(message):
    try:
        amount = float(message.text)
        chat_id = message.chat.id
        if chat_id in user_states:
            currency_pair = user_states[chat_id]['currency_pair']
            base_currency = currency_pair[0]
            target_currency = currency_pair[1]
            rate = get_exchange_rate(base_currency, target_currency)
            if rate is not None:
                converted_amount = amount * rate
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('🔄 Конвертировать другую валюту', callback_data='next_currency')
                btn2 = types.InlineKeyboardButton('✅ Завершить', callback_data='finish_conversion')
                markup.add(btn1, btn2)
                bot.send_message(chat_id, f"Результат: {amount} {base_currency} = {converted_amount:.2f} {target_currency}", reply_markup=markup)
            else:
                # Если не удалось получить курс валют
                markup = types.InlineKeyboardMarkup()
                btn_return = types.InlineKeyboardButton('Вернуться в каталог', callback_data='return_to_catalog')
                markup.add(btn_return)
                bot.send_message(chat_id, "Не удалось получить курс валют. Попробуйте позже.", reply_markup=markup)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
def finish_conversion(callback):
    if callback.message.chat.id in user_states:
        del user_states[callback.message.chat.id]
    bot.send_message(callback.message.chat.id, "Конвертация завершена.")
    return_to_catalog(callback.message)  # Передаем callback.message вместо callback
def cancel_catalog(callback):
            # Сбрасываем состояние пользователя
    user_states.pop(callback.message.chat.id, None)
            # Отправляем сообщение о завершении
    bot.send_message(callback.message.chat.id, "Каталог закрыт.")

            # Возвращаем пользователя в главное меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Каталог действий')
    markup.row(btn1)
    bot.send_message(callback.message.chat.id, "Вы вернулись в главное меню.", reply_markup=markup)
    bot.register_next_step_handler(callback.message, click)







bot.infinity_polling(timeout=30)
