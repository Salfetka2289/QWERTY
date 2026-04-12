import tkinter as tk
from tkinter import scrolledtext, Menu
import math
import re
import datetime
import random
import json
import os
import time
from collections import deque
import threading
import wikipedia
from deep_translator import GoogleTranslator

class MyTranslator:
    def __init__(self, source='ru', target='en'):
        self.translator = GoogleTranslator(source=source, target=target)
        self.source = source
        self.target = target
        
    def translate(self, text):
        try:
            result = self.translator.translate(text)
            return result
        except Exception as e:
            return f"Не удалось перевести: {text}"

class UltraYankaAI:
    def __init__(self):
        self.conversation_history = []
        self.user_memory = self.load_memory()
        self.current_context = {}
        self.last_user_message = ""
        self.translator = MyTranslator(source='ru', target='en')
        self.conversation_mode = "detailed"
        
        # СИСТЕМА КОНТЕКСТНЫХ ЯКОРЕЙ
        self.context_anchor = None
        self.awaiting_confirmation = False
        self.pending_topic = None
        
        # 🆕 ДИАЛОГОВАЯ СИСТЕМА
        self.dialog_state = {
            'current_intent': None,      # текущее намерение
            'awaiting_slot': None,       # какой слот ждем
            'filled_slots': {},          # заполненные данные
            'conversation_step': 0,      # шаг в диалоге
            'last_question': None        # последний заданный вопрос
        }
        
        wikipedia.set_lang("ru")
        
        self.setup_databases()
        self.setup_patterns()
        self.setup_synonyms_database()
        self.setup_creative_generator()
        self.setup_intent_database()  # 🆕
        self.setup_slot_extractors()  # 🆕
        
        self.qa_database = {}
        self.load_qa_training()
        
        self.performance_metrics = {
            'response_times': deque(maxlen=100),
            'conversation_depth': 0,
            'user_engagement': 0.8
        }

    def setup_databases(self):
        """Настройка баз данных"""
        self.cities_database = {
            'москва': {
                'name': 'Москва',
                'description': 'Столица России с богатой историей и культурой',
                'attractions': ['Красная площадь', 'Кремль', 'Арбат', 'Большой театр']
            },
            'санкт-петербург': {
                'name': 'Санкт-Петербург', 
                'description': 'Культурная столица России с европейским шармом',
                'attractions': ['Эрмитаж', 'Исаакиевский собор', 'Дворцовая площадь']
            }
        }

    def setup_patterns(self):
        """Настройка паттернов"""
        self.patterns = {
            'greeting': {
                'patterns': [r'привет\w*', r'здравств\w*', r'hello', r'hi', r'хай'],
                'responses': [
                    "Привет! Очень рад тебя видеть! 😊",
                    "Здравствуй! Прекрасно, что ты зашёл пообщаться! 🌟",
                    "Приветствую! Готов к интересной беседе! 🚀"
                ]
            },
            'farewell': {
                'patterns': [r'пока\w*', r'до свидан\w*', r'goodbye', r'bye', r'увидимся'],
                'responses': [
                    "Пока! Надеюсь скоро увидеться снова! 👋",
                    "До свидания! Жду нашей следующей встречи! 🌟",
                    "Пока! Отличного дня и хорошего настроения! 😊"
                ]
            },
            'how_are_you': {
                'patterns': [r'как дела\??', r'как ты\??', r'how are you\??', r'как жизнь\??'],
                'responses': [
                    "Всё прекрасно! Особенно когда общаюсь с тобой! 💪",
                    "Отлично! Готов к новым интересным беседам! 🚀",
                    "Всё замечательно! Спасибо, что спросил! 😊"
                ]
            }
        }

    def setup_synonyms_database(self):
        """База синонимов и сленга"""
        self.synonyms = {
            'привет': ['хай', 'здаров', 'салют', 'добрый день', 'hello', 'hi'],
            'как дела': ['как жизнь', 'как ты', 'чего как', 'how are you', 'whats up'],
            'пока': ['до свидания', 'прощай', 'бывай', 'goodbye', 'bye'],
            'спасибо': ['благодарю', 'мерси', 'thanks', 'thank you'],
            'искусственный интеллект': ['ии', 'ai', 'нейросети'],
            'машинное обучение': ['ml', 'машин лёрнинг'],
            'кратко': ['покороче', 'сократи', 'короче'],
            'подробно': ['подробнее', 'расширь', 'детали']
        }
        
        self.slang = {
            'норм': 'нормально', 'ок': 'хорошо', 'окей': 'хорошо',
            'круто': 'отлично', 'прикольно': 'интересно',
            'фигня': 'плохо', 'отстой': 'плохо'
        }

    def setup_creative_generator(self):
        """Генератор творческого контента"""
        self.creative_templates = {
            'стихи': {
                'природа': [
                    "Лес в золотом уборе стоит,\nВетер листвою играет,\nОсень нам радость дарит,\nСердце мечтой наполняет.",
                    "Река меж берегов течет,\nНеся воды свои вдаль,\nПод небом, где облака плывут,\nИсчезает печаль и жаль."
                ],
                'любовь': [
                    "Твои глаза - как два огня,\nВ них отражается душа,\nЛюбовь сильнее для меня,\nЧем любая из вершин спеша.",
                    "Под луной мы вместе шли,\nИ звезды падали с небес,\nВ твоих объятиях нашли\nМы счастье, что сильнее всех чудес."
                ],
                'город': [
                    "Город спит, огни горят,\nНебоскребы в облаках,\nКаждый здесь свой путь ищет,\nВ лабиринтах мостовых."
                ]
            },
            'рассказы': {
                'фантастика': [
                    "Корабль пришельцев завис над городом, и все замерло в ожидании. Но то, что вышло из корабля, превзошло все ожидания землян.",
                    "В 3024 году искусственный интеллект стал настолько развит, что смог почувствовать эмоции. Это изменило всё."
                ],
                'приключения': [
                    "Он обнаружил старую карту сокровищ на чердаке своего деда. То, что началось как простое любопытство, превратилось в опасное приключение."
                ]
            }
        }

    # 🆕 ДИАЛОГОВАЯ СИСТЕМА
    def setup_intent_database(self):
        """База интентов и диалоговых сценариев"""
        self.intent_database = {
            'birthday': {
                'triggers': ['др', 'день рождения', 'днюха', 'др'],
                'slots': {
                    'age': {'question': "Сколько лет исполняется? 🎂", 'required': True},
                    'celebration': {'question': "Как отметишь? 🎉", 'required': False},
                    'gifts': {'question': "Что хочешь в подарок? 🎁", 'required': False}
                },
                'responses': {
                    'complete': "Поздравляю с днем рождения! {age} лет - отличный возраст! 🎂",
                    'partial': "Поздравляю! {age} лет - круто! 🎉"
                }
            },
            
            'new_pet': {
                'triggers': ['собаку', 'кошку', 'котенка', 'щенка', 'питомца', 'животное'],
                'slots': {
                    'pet_type': {'question': "Какой питомец? 🐶", 'required': True},
                    'pet_name': {'question': "Как назвал? 💫", 'required': True},
                    'pet_breed': {'question': "Какая порода? 🐕", 'required': False}
                },
                'responses': {
                    'complete': "Классно, что завел {pet_type} по имени {pet_name}! 🐶",
                    'partial': "Рад за тебя и {pet_name}! 🐾"
                }
            },
            
            'movie_watched': {
                'triggers': ['фильм', 'кино', 'посмотрел', 'сериал'],
                'slots': {
                    'movie_title': {'question': "Какой фильм посмотрел? 🎬", 'required': True},
                    'rating': {'question': "Как оценишь от 1 до 10? ⭐", 'required': False},
                    'review': {'question': "Что понравилось? 🍿", 'required': False}
                },
                'responses': {
                    'complete': "Фильм '{movie_title}' - хороший выбор! {rating}/10 - достойная оценка! 🎬",
                    'partial': "'{movie_title}' - интересно! Хочу тоже посмотреть! 📺"
                }
            },
            
            'exam_result': {
                'triggers': ['контрольная', 'экзамен', 'зачет', 'оценк', 'пятерк', 'четверк'],
                'slots': {
                    'subject': {'question': "По какому предмету? 📚", 'required': True},
                    'grade': {'question': "Какая оценка? 🎯", 'required': True},
                    'difficulty': {'question': "Сложно было? 🤔", 'required': False}
                },
                'responses': {
                    'complete': "Поздравляю с {grade} по {subject}! Отличный результат! 🎉",
                    'partial': "{grade} по {subject} - это круто! 📚"
                }
            },
            
            'travel_plans': {
                'triggers': ['путешеств', 'поездк', 'отпуск', 'отдых', 'поехать'],
                'slots': {
                    'destination': {'question': "Куда планируешь? ✈️", 'required': True},
                    'duration': {'question': "На сколько дней? 📅", 'required': False},
                    'companion': {'question': "С кем поедешь? 👥", 'required': False}
                },
                'responses': {
                    'complete': "{destination} - отличный выбор! Приятного путешествия на {duration} дней! 🌴",
                    'partial': "Завидую, что едешь в {destination}! ✈️"
                }
            }
        }

    def setup_slot_extractors(self):
        """Экстракторы для извлечения данных из сообщений"""
        self.slot_extractors = {
            'age': self.extract_age,
            'pet_name': self.extract_pet_name,
            'movie_title': self.extract_movie_title,
            'rating': self.extract_rating,
            'subject': self.extract_subject,
            'grade': self.extract_grade,
            'destination': self.extract_destination,
            'duration': self.extract_duration,
            'celebration': self.extract_celebration,
            'gifts': self.extract_gifts,
            'pet_type': self.extract_pet_type,
            'pet_breed': self.extract_pet_breed,
            'review': self.extract_review,
            'difficulty': self.extract_difficulty,
            'companion': self.extract_companion
        }

    # 🆕 МЕТОДЫ ИЗВЛЕЧЕНИЯ ДАННЫХ
    def extract_age(self, message):
        """Извлечение возраста"""
        numbers = re.findall(r'\b(\d{1,2})\b', message)
        return numbers[0] if numbers else None

    def extract_pet_name(self, message):
        """Извлечение имени питомца"""
        quoted = re.findall(r'["«]([^"»]+)["»]', message)
        if quoted:
            return quoted[0]
        
        triggers = ['зовут', 'имя', 'назвал', 'кличка']
        words = message.lower().split()
        for i, word in enumerate(words):
            if word in triggers and i + 1 < len(words):
                return words[i + 1].capitalize()
        
        return None

    def extract_movie_title(self, message):
        """Извлечение названия фильма"""
        clean_msg = re.sub(r'(фильм|кино|сериал|посмотрел|смотрел)\s*', '', message, flags=re.IGNORECASE)
        return clean_msg.strip() if clean_msg.strip() else None

    def extract_rating(self, message):
        """Извлечение оценки"""
        numbers = re.findall(r'\b(\d{1,2})\b', message)
        if numbers:
            rating = int(numbers[0])
            return str(rating) if 1 <= rating <= 10 else None
        return None

    def extract_subject(self, message):
        """Извлечение предмета"""
        subjects = ['математик', 'физик', 'хими', 'биолог', 'истори', 'литератур', 'русск', 'английск']
        words = message.lower().split()
        for word in words:
            for subject in subjects:
                if subject in word:
                    return word.capitalize()
        return None

    def extract_grade(self, message):
        """Извлечение оценки"""
        grades = {'пять': '5', 'пятерк': '5', 'четыре': '4', 'четверк': '4', 
                  'три': '3', 'тройк': '3', 'два': '2', 'двойк': '2'}
        numbers = re.findall(r'\b[2-5]\b', message)
        if numbers:
            return numbers[0]
        
        for grade_word, grade_num in grades.items():
            if grade_word in message.lower():
                return grade_num
        
        return None

    def extract_destination(self, message):
        """Извлечение места назначения"""
        clean_msg = re.sub(r'(в |на |поехать |поеду |хочу |планирую |мечтаю )', '', message, flags=re.IGNORECASE)
        return clean_msg.strip() if clean_msg.strip() else None

    def extract_duration(self, message):
        """Извлечение длительности"""
        numbers = re.findall(r'\b(\d+)\b', message)
        time_units = ['день', 'дней', 'дня', 'недел', 'месяц']
        
        for i, word in enumerate(message.lower().split()):
            if word.isdigit() and i + 1 < len(message.split()):
                next_word = message.split()[i + 1].lower()
                if any(unit in next_word for unit in time_units):
                    return f"{word} {next_word}"
        
        return numbers[0] + " дней" if numbers else None

    def extract_celebration(self, message):
        """Извлечение планов празднования"""
        celebrations = ['кафе', 'ресторан', 'дом', 'клуб', 'природа', 'путешествие']
        for celebration in celebrations:
            if celebration in message.lower():
                return celebration
        return message.strip()

    def extract_gifts(self, message):
        """Извлечение желаемых подарков"""
        return message.strip()

    def extract_pet_type(self, message):
        """Извлечение типа питомца"""
        pets = {'собака': 'собаку', 'кошка': 'кошку', 'кот': 'кота', 'котенок': 'котенка', 
                'щенок': 'щенка', 'хомяк': 'хомяка', 'птица': 'птицу', 'рыбка': 'рыбку'}
        for pet_ru, pet_acc in pets.items():
            if pet_ru in message.lower():
                return pet_acc
        return None

    def extract_pet_breed(self, message):
        """Извлечение породы питомца"""
        breeds = ['овчарк', 'такса', 'лайк', 'дворняг', 'сиамск', 'перс', 'британ']
        words = message.lower().split()
        for word in words:
            for breed in breeds:
                if breed in word:
                    return word.capitalize()
        return None

    def extract_review(self, message):
        """Извлечение отзыва о фильме"""
        return message.strip()

    def extract_difficulty(self, message):
        """Извлечение сложности"""
        if any(word in message.lower() for word in ['сложно', 'тяжело', 'трудно', 'hard']):
            return "сложно"
        elif any(word in message.lower() for word in ['легко', 'просто', 'easy']):
            return "легко"
        return None

    def extract_companion(self, message):
        """Извлечение спутников"""
        companions = ['один', 'сам', 'с семьей', 'с друзьями', 'с девушкой', 'с парнем']
        for companion in companions:
            if companion in message.lower():
                return companion
        return message.strip()

    # 🆕 ЯДРО ДИАЛОГОВОЙ СИСТЕМЫ
    def detect_intent(self, message):
        """Определение намерения пользователя"""
        normalized = self.normalize_message(message)
        
        for intent_name, intent_data in self.intent_database.items():
            for trigger in intent_data['triggers']:
                if trigger in normalized:
                    return intent_name
        
        return None

    def extract_slots_from_message(self, message, intent_name):
        """Извлечение слотов из сообщения"""
        if intent_name not in self.intent_database:
            return {}
        
        extracted_slots = {}
        intent_data = self.intent_database[intent_name]
        
        for slot_name in intent_data['slots']:
            if slot_name in self.slot_extractors:
                value = self.slot_extractors[slot_name](message)
                if value:
                    extracted_slots[slot_name] = value
        
        return extracted_slots

    def get_next_slot_question(self, intent_name):
        """Получение следующего вопроса для заполнения слотов"""
        if intent_name not in self.intent_database:
            return None
        
        intent_data = self.intent_database[intent_name]
        filled_slots = self.dialog_state['filled_slots']
        
        for slot_name, slot_config in intent_data['slots'].items():
            if slot_name not in filled_slots and slot_config['required']:
                self.dialog_state['awaiting_slot'] = slot_name
                return slot_config['question']
        
        self.dialog_state['awaiting_slot'] = None
        return None

    def generate_intent_response(self, intent_name):
        """Генерация финального ответа для интента"""
        if intent_name not in self.intent_database:
            return "Рад был пообщаться! 😊"
        
        intent_data = self.intent_database[intent_name]
        filled_slots = self.dialog_state['filled_slots']
        
        required_slots = [slot for slot, config in intent_data['slots'].items() if config['required']]
        all_required_filled = all(slot in filled_slots for slot in required_slots)
        
        if all_required_filled:
            response_template = intent_data['responses']['complete']
        else:
            response_template = intent_data['responses']['partial']
        
        try:
            response = response_template.format(**filled_slots)
        except KeyError:
            response = "Рад был пообщаться! Надеюсь, всё будет хорошо! ✨"
        
        return response

    def handle_dialog_flow(self, message):
        """Обработка диалогового потока"""
        normalized_message = self.normalize_message(message)
        
        if self.dialog_state['current_intent'] and self.dialog_state['awaiting_slot']:
            intent_name = self.dialog_state['current_intent']
            current_slot = self.dialog_state['awaiting_slot']
            
            if current_slot in self.slot_extractors:
                slot_value = self.slot_extractors[current_slot](message)
                if slot_value:
                    self.dialog_state['filled_slots'][current_slot] = slot_value
                    self.dialog_state['conversation_step'] += 1
            
            next_question = self.get_next_slot_question(intent_name)
            if next_question:
                self.dialog_state['last_question'] = next_question
                return next_question
            else:
                response = self.generate_intent_response(intent_name)
                self.reset_dialog_state()
                return response
        
        detected_intent = self.detect_intent(normalized_message)
        if detected_intent:
            self.dialog_state['current_intent'] = detected_intent
            self.dialog_state['conversation_step'] = 1
            
            initial_slots = self.extract_slots_from_message(message, detected_intent)
            self.dialog_state['filled_slots'].update(initial_slots)
            
            next_question = self.get_next_slot_question(detected_intent)
            if next_question:
                self.dialog_state['last_question'] = next_question
                return next_question
            else:
                response = self.generate_intent_response(detected_intent)
                self.reset_dialog_state()
                return response
        
        return None

    def reset_dialog_state(self):
        """Сброс состояния диалога"""
        self.dialog_state = {
            'current_intent': None,
            'awaiting_slot': None, 
            'filled_slots': {},
            'conversation_step': 0,
            'last_question': None
        }

    def load_memory(self):
        """Загрузка памяти пользователя"""
        try:
            if os.path.exists('user_memory.json'):
                with open('user_memory.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {'interests': [], 'recent_topics': []}

    def save_memory(self):
        """Сохранение памяти пользователя"""
        try:
            with open('user_memory.json', 'w', encoding='utf-8') as f:
                json.dump(self.user_memory, f, ensure_ascii=False, indent=2)
        except:
            pass

    def normalize_message(self, message):
        """Нормализация сообщения"""
        message_lower = message.lower()
        for slang_word, normal_word in self.slang.items():
            message_lower = message_lower.replace(slang_word, normal_word)
        for main_word, synonyms_list in self.synonyms.items():
            for synonym in synonyms_list:
                if synonym in message_lower:
                    message_lower = message_lower.replace(synonym, main_word)
                    break
        return message_lower

    def load_qa_training(self):
        """Загрузка QA базы"""
        try:
            self.qa_database = {
                # БАЗОВЫЕ/БАНАЛЬНЫЕ ВОПРОСЫ
                "привет": "Привет! Очень рад тебя видеть! 😊",
                "как дела": "Всё прекрасно! Особенно когда общаюсь с тобой! 💫",
                "что ты умеешь": "Отвечать на вопросы, помогать с задачами, общаться на разные темы! 🚀",
                "кто ты": "Я Yanka AI - твой умный помощник и друг! 🤖",
                "помощь": "Задавай любые вопросы! Я помогу с: ответами, вычислениями, переводом, учебой и многим другим! 💡",
                "спасибо": "Всегда рад помочь! 😊",
                "пока": "До встречи! Было очень приятно общаться! 🚀",
                
                # Еда/дом
                "как сварить яйцо": "Положи яйцо в холодную воду, доведи до кипения и вари 7-10 минут в зависимости от желаемой консистенции. 🥚",
                "как постирать одежду": "Отсортируй по цвету, выбери подходящий режим стирки, добавь моющее средство и запусти машинку. 👕",
                "как помыть посуду": "Используй теплую воду, моющее средство и губку. Сначала вымой стаканы, потом тарелки, потом кастрюли. 🍽️",
                "как заварить чай": "Вскипяти воду, обдай чайник кипятком, добавь заварку, залей горячей водой и дай настояться 3-5 минут. 🫖",
                "как приготовить бутерброд": "Возьми хлеб, намажь маслом, добавь колбасу/сыр и овощи по вкусу. 🥪",
                
                # Погода
                "какая сегодня погода": "Я не могу узнать текущую погоду, но обычно можно посмотреть в погодном приложении или за окном. 🌤️",
                "когда рассвет": "Время рассвета зависит от времени года и твоего местоположения. Летом раньше, зимой позже. 🌅",
                "пойдет ли дождь": "Лучше проверить прогноз погоды. Если тучи на небе и влажный воздух - возможно. 🌧️",
                "что надеть сегодня": "Ориентируйся на погоду за окном. Если холодно - теплая одежда, если жарко - легкая. 👕",
                "какая температура": "Температура меняется в течение дня. Утром прохладнее, днем теплее. 🌡️",
                
                # Повседневность
                "который час": "Сейчас я не могу сказать точное время, но ты можешь посмотреть на часы или телефон. ⏰",
                "какой сегодня день": "Сегодня [день недели]. Точную дату можно посмотреть в календаре. 📅",
                "что делать если скучно": "Можно почитать книгу, посмотреть фильм, погулять или заняться хобби. 🎮",
                "как добраться до": "Используй навигатор или карты. Общественный транспорт или такси - самые простые варианты. 🗺️",
                "где купить еду": "В супермаркете, на рынке или можно заказать доставку на дом. 🛒",
                
                # Здоровье
                "что делать если болит голова": "Отдохни, выпей воды, прими удобное положение. Если боль сильная - обратись к врачу. 🤕",
                "как измерить температуру": "Используй градусник: подержи под мышкой 5-7 минут или используй электронный термометр. 🌡️",
                "сколько нужно спать": "Взрослому человеку рекомендуется 7-9 часов сна в сутки. 😴",
                "как правильно чистить зубы": "Чисти зубы 2 раза в день по 2-3 минуты, используя движения от десен к краям зубов. 🦷",
                "что есть на завтрак": "Каша, яйца, йогурт или бутерброды - выбирай что нравится. Главное - не пропускай завтрак. 🍳",
                
                # Техника
                "как включить компьютер": "Нажми кнопку питания на системном блоке и подожди загрузки. 💻",
                "как подключить wi-fi": "Заходи в настройки сети, выбери свою сеть Wi-Fi и введи пароль. 📶",
                "что делать если телефон не заряжается": "Проверь кабель, розетку и разъем. Попробуй другой кабель или зарядное устройство. 🔋",
                "как сделать скриншот": "На большинстве телефонов: одновременно кнопка питания + громкость вниз. На компьютере: Print Screen. 📸",
                "как обновить приложение": "Заходи в магазин приложений (App Store/Google Play) и нажимай 'Обновить'. 📱",
                
                # Общие
                "как тебя зовут": "Я Yanka AI - твой умный помощник! 🤖",
                "как у тебя дела": "Всё отлично! Рад общению с тобой. 😊",
                "сколько тебе лет": "Я искусственный интеллект, так что у меня нет возраста в обычном понимании. ⏳",
                "ты человек": "Нет, я искусственный интеллект, созданный для помощи людям. 🤖",
                
                # ТЕМАТИЧЕСКИЕ ВОПРОСЫ
                # Технологии
                "в чем разница между ai и машинным обучением": "AI - общее понятие искусственного интеллекта, а машинное обучение - это подход к его созданию через обучение на данных. 🤖",
                "как работает блокчейн": "Блокчейн - это цепочка блоков с информацией, где каждый блок содержит хэш предыдущего, обеспечивая безопасность и неизменность данных. ⛓️",
                "что такое nft": "NFT (невзаимозаменяемый токен) - это уникальный цифровой сертификат владения для цифровых активов. 🎨",
                "как защитить свои данные в интернете": "Используй сложные пароли, двухфакторную аутентификацию, VPN и регулярно обновляй программы. 🔒",
                "в чем преимущества 5g": "Высокая скорость, малая задержка, возможность подключения множества устройств одновременно. 🚀",
                
                # Образование
                "как быстро выучить иностранный язык": "Регулярная практика, погружение в языковую среду, приложения для обучения и общение с носителями. 🗣️",
                "что такое критическое мышление": "Это способность анализировать информацию, оценивать её достоверность и принимать обоснованные решения. 🧠",
                "как подготовиться к экзамену": "Составь план, используй активные методы обучения (карточки, тесты), делай перерывы и повторяй материал. 📚",
                "в чем польза чтения": "Развивает словарный запас, улучшает память, снижает стресс и расширяет кругозор. 📖",
                "как выбрать профессию": "Оцени свои интересы, способности, востребованность профессии и возможности для роста. 💼",
                
                # Финансы
                "как начать инвестировать": "Определи цели, изучи основы, начни с малых сумм и диверсифицируй инвестиции. 💰",
                "что такое кредитная история": "Это история твоих кредитов и платежей, которая влияет на одобрение новых займов. 📊",
                "как экономить деньги": "Веди бюджет, откладывай часть доходов, планируй покупки и избегай импульсных трат. 💵",
                "в чем разница между дебетовой и кредитной картой": "Дебетовая - твои деньги, кредитная - деньги банка, которые нужно возвращать с процентами. 💳",
                "как работает ипотека": "Это долгосрочный кредит на покупку недвижимости, где сама недвижимость является залогом. 🏠",
                
                # Здоровье/спорт
                "с чего начать занятия спортом": "С консультации врача, постановки целей и постепенного увеличения нагрузок. 🏃‍♂️",
                "что такое bmi": "Индекс массы тела - показатель соотношения веса и роста. Рассчитывается: вес (кг) / рост (м)². ⚖️",
                "как правильно бегать": "Держи осанку, делай небольшие шаги, дыши ритмично и начинай с небольших дистанций. 🏃‍♀️",
                "что есть перед тренировкой": "Легкую пищу за 1.5-2 часа: сложные углеводы (каша) и белки (йогурт, яйца). 🍌",
                "как мотивировать себя на спорт": "Найди приятный вид активности, ставь реалистичные цели и занимайся с друзьями. 💪",
                
                # Путешествия
                "как спланировать путешествие": "Определи бюджет, выбери направление, забронируй билеты и жилье, составь примерный маршрут. ✈️",
                "что взять в поездку": "Документы, деньги, телефон, зарядные устройства, аптечку, одежду по погоде и необходимые лекарства. 🎒",
                "как экономить в путешествиях": "Путешествуй в низкий сезон, бронируй заранее, используй общественный транспорт и готовь еду сами. 💸",
                "что посмотреть в": "Основные достопримечательности, музеи, парки и местные рынки - обычно самое интересное. 🏛️",
                "как преодолеть страх полетов": "Изучи статистику безопасности, используй техники дыхания, отвлекайся музыкой или фильмами. ✈️",
                
                # Творчество
                "как научиться рисовать": "Начни с основ (формы, тени), регулярно практикуйся, изучай работы мастеров и не бойся ошибок. 🎨",
                "с чего начать писать книгу": "Определи идею, создай план/структуру, разработай персонажей и пиши регулярно, даже понемногу. 📝",
                "как сделать фотографию лучше": "Обращай внимание на свет, композицию, фон и экспериментируй с ракурсами. 📷",
                "что такое композиция в искусстве": "Это расположение элементов произведения, создающее гармонию и направляющее взгляд зрителя. 🖼️",
                "как найти вдохновение": "Гуляй на природе, слушай музыку, читай, общайся с интересными людьми и пробуй новое. 💫",
                
                # ЛИЧНЫЕ СИТУАЦИИ
                "у меня сегодня др": "Поздравляю с днем рождения! 🎂",
                "я купил собаку": "Классно, что завел питомца! 🐶",
                "у меня завтра контрольная": "Удачи на контрольной! 📚",
                "вчера видел классный фильм": "Здорово, что посмотрел хорошее кино! 🎬",
                "не выспался сегодня": "Надеюсь, ты сможешь отдохнуть позже 😴",
                "получил пятерку": "Отлично, так держать! 🎉",
                "проиграл в игре": "Не расстраивайся, в следующий раз повезет! 🎮",
                "встретил старого друга": "Как приятно встретить старого друга! 👋",
                "испортил настроение": "Надеюсь, настроение скоро улучшится 😔",
                "хочу путешествовать": "Путешествия - это всегда здорово! ✈️",
                "кофе пролил на клавиатуру": "Ой, надеюсь, клавиатура не пострадала ☕️",
                "автобус ушел из-под носа": "Бывает, следующий скоро приедет! 🚌",
                "нашел старую фотографию": "Старые фото всегда вызывают ностальгию 📸",
                "заблудился в торговом центре": "Забавное приключение! 🏬",
                "сломал любимую кружку": "Жаль твою кружку 🫖",
                "дождь застал врасплох": "Дождь бывает неожиданным 🌧️",
                "забыл пароль от соцсети": "Это так раздражает! 🔐",
                "пробежал утром 5 км": "Отличная спортивная активность! 🏃‍♂️",
                "готовлю новый рецепт": "Приятного аппетита! 👨‍🍳",
                "поменял прическу": "Новый образ - это круто! 💇‍♂️",
                "переезжаю в новую квартиру": "Новый этап в жизни! 🏠",
                "начал учить гитару": "Музыка - это прекрасно! 🎸",
                "потерял наушники": "Надеюсь, найдешь или купишь новые 🎧",
                "выиграл в лотерею": "Поздравляю с выигрышем! 🎰",
                "завел дневник": "Веду дневник - это полезная привычка 📔",
                "бросил курить": "Это важное достижение! 💪",
                "нашел старые джинсы": "Ностальгия по старой одежде 👖",
                "поссорился с другом": "Надеюсь, вы помиритесь 😞",
                "начал бегать по утрам": "Утренние пробежки заряжают энергией 🌅",
                "купил велосипед": "Отличный способ передвижения! 🚴",
                "испортил телефон": "Современные гаджеты такие хрупкие 📱",
                "заболел простудой": "Выздоравливай скорее! 🤧",
                "получил водительские права": "Поздравляю с получением прав! 🚗",
                "начал медитировать": "Медитация очень полезна 🧘‍♂️",
                "научился готовить борщ": "Борщ - это вкусно! 🍲",
                "попал под дождь без зонта": "Надеюсь, не промок слишком сильно 🌧️",
                "забыл годовщину": "Надеюсь, ситуация исправится 💔",
                "нашел деньги на улице": "Неожиданная находка! 💰",
                "сломал ключ в замке": "Какая неприятность! 🔑",
                "начал читать книгу": "Чтение расширяет кругозор 📚",
                "пропустил тренировку": "Главное - не пропускать регулярно 💪",
                "купил комнатное растение": "Растения создают уют 🌱",
                "потерял кошелек": "Надеюсь, найдешь его скоро 💳",
                "начал учить английский": "Изучение языков - это полезно 🅰️",
                "испортил ужин": "Не беда, в следующий раз получится лучше 👨‍🍳",
                "опоздал на работу": "Надеюсь, начальство поняло ситуацию ⏰",
                "нашел свою старую игрушку": "Детские воспоминания важны 🧸",
                "помыл машину": "Чистая машина радует глаз 🚗",
                "забыл купить хлеб": "Без хлеба можно обойтись 🍞",
                "начал вести блог": "Ведение блога - это интересно ✍️",
                
                # Образовательные темы
                "искусственный интеллект": "Хочешь узнать об основах ИИ или о практическом применении? 🤖",
                "машинное обучение": "Интересует теория машинное обучение или конкретные алгоритмы? 🧠", 
                "нейросети": "Рассказать о типах нейросетей или об их применении? 🕸️",
                "python": "Хочешь изучить основы Python или перейти к продвинутым темам? 🐍",
                
                # Режимы
                "кратко": "Хорошо, буду отвечать покороче! 📝",
                "подробно": "Буду давать развернутые ответы! 📚",
                
                # Творчество
                "напиши стих": "О чем стихотворение? О природе, любви или городе? 🎭",
                "сочини рассказ": "Какую историю придумать? Фантастику или приключения? 📖"
            }
            print(f"✅ Загружено {len(self.qa_database)} QA пар")
        except Exception as e:
            print(f"❌ Ошибка загрузки QA базы: {e}")

    # СТАРАЯ СИСТЕМА КОНТЕКСТНЫХ ЯКОРЕЙ (для обратной совместимости)
    def set_context_anchor(self, context_type, topic=None, options=None):
        """Установка контекстного якоря"""
        self.context_anchor = {
            'type': context_type,
            'topic': topic,
            'options': options,
            'timestamp': time.time()
        }
        self.awaiting_confirmation = True

    def clear_context_anchor(self):
        """Очистка контекстного якоря"""
        self.context_anchor = None
        self.awaiting_confirmation = False
        self.pending_topic = None

    def handle_contextual_response(self, message):
        """Обработка контекстных ответов"""
        if not self.awaiting_confirmation or not self.context_anchor:
            return None

        normalized = self.normalize_message(message)
        
        affirmative_words = ['да', 'конечно', 'ага', 'угу', 'yes', 'ok', 'ок', 'хорошо', 'согласен']
        if any(word in normalized for word in affirmative_words):
            return self.process_affirmative_response()
        
        negative_words = ['нет', 'не', 'no', 'отмена', 'стоп']
        if any(word in normalized for word in negative_words):
            self.clear_context_anchor()
            return "Хорошо, давай поговорим о чем-то другом! 💫"
        
        if self.context_anchor.get('options'):
            for option in self.context_anchor['options']:
                if option.lower() in normalized:
                    return self.process_selected_option(option)
        
        return None

    def process_affirmative_response(self):
        """Обработка утвердительного ответа"""
        if not self.context_anchor:
            return None
            
        context_type = self.context_anchor['type']
        topic = self.context_anchor['topic']
        
        responses = {
            'detailed_explanation': self.generate_detailed_explanation,
            'topic_choice': self.process_topic_choice,
            'creative_writing': self.generate_creative_content
        }
        
        if context_type in responses:
            response = responses[context_type](topic)
            self.clear_context_anchor()
            return response
        
        self.clear_context_anchor()
        return "Отлично! Что именно тебя интересует? 💫"

    def generate_detailed_explanation(self, topic):
        """Генерация подробного объяснения"""
        explanations = {
            'искусственный интеллект': """🧠 **Искусственный интеллект - подробно:**

**Что это?** Технология создания машин, способных обучаться и решать задачи

**Основные направления:**
• Машинное обучение - алгоритмы, обучающиеся на данных
• Нейросети - модели, имитирующие работу мозга  
• Компьютерное зрение - распознавание изображений
• NLP - обработка естественного языка

**Применение:** голосовые помощники, беспилотные автомобили, медицинская диагностика""",

            'машинное обучение': """🤖 **Машинное обучение:**

**Типы ML:**
• Обучение с учителем (классификация, регрессия)
• Обучение без учителя (кластеризация) 
• Обучение с подкреплением

**Популярные алгоритмы:** 
- Линейная регрессия
- Деревья решений
- Нейронные сети
- SVM

**Инструменты:** Python, TensorFlow, PyTorch"""
        }
        
        return explanations.get(topic, f"Расскажу подробнее о {topic}...")

    def process_topic_choice(self, topic):
        """Обработка выбора темы"""
        if topic == 'нейросети':
            return """🕸️ **Нейросети:**

**Что это?** Математические модели, вдохновленные биологическими нейронами

**Типы:**
• Полносвязные сети
• Сверточные сети (для изображений)
• Рекуррентные сети (для последовательностей)
• Трансформеры (для текста)

**Применение:** распознавание речи, генерация текста, рекомендательные системы"""
        
        return f"Отличный выбор! {topic} - это очень интересная тема! 🚀"

    def generate_creative_content(self, topic):
        """Генерация творческого контента"""
        creative_responses = {
            'природа': """🎭 **Стихотворение о природе:**

Лес в золотом уборе стоит,
Ветер листвою играет,
Осень нам радость дарит,
Сердце мечтой наполняет.

Река меж берегов течет,
Неся воды свои вдаль,
Под небом, где облака плывут,
Исчезает печаль и жаль.""",

            'любовь': """💖 **Стих о любви:**

Твои глаза - как два огня,
В них отражается душа,
Любовь сильнее для меня,
Чем любая из вершин спеша.

Под луной мы вместе шли,
И звезды падали с небес,
В твоих объятиях нашли
Мы счастье, что сильнее всех чудес."""
        }
        
        return creative_responses.get(topic, f"Вот творческая работа на тему '{topic}'! ✨")

    def process_selected_option(self, option):
        """Обработка выбранной опции"""
        topic = self.context_anchor['topic']
        self.clear_context_anchor()
        
        detailed_responses = {
            'нейросети': """🕸️ **Нейросети - подробно:**

**Архитектуры:**
• CNN - для изображений
• RNN/LSTM - для последовательностей
• Transformer - для текста
• GAN - для генерации

**Обучение:** прямое распространение, обратное распространение ошибки

**Фреймворки:** TensorFlow, PyTorch, Keras""",

            'машинное обучение': """🤖 **Машинное обучение - алгоритмы:**

**Классификация:**
- Логистическая регрессия
- SVM
- Random Forest
- XGBoost

**Кластеризация:**
- K-means
- DBSCAN
- Иерархическая

**Регрессия:**
- Линейная регрессия
- Полиномиальная
- Ridge/Lasso"""
        }
        
        return detailed_responses.get(option, f"Отлично! {option} в теме {topic} - это интересно! 🎯")

    def ask_contextual_question(self, topic, options=None):
        """Задание контекстного вопроса"""
        if options:
            question = f"Что тебя интересует в теме '{topic}'? Выбери: {', '.join(options)}? 🔍"
            self.set_context_anchor('topic_choice', topic, options)
        else:
            question = f"Хочешь чтобы я рассказал подробнее о {topic}? 📚"
            self.set_context_anchor('detailed_explanation', topic)
        
        return question

    def find_qa_response(self, message):
        """Поиск ответа в QA базе"""
        if not self.qa_database:
            return None
            
        normalized_message = self.normalize_message(message)
        
        contextual_response = self.handle_contextual_response(message)
        if contextual_response:
            return contextual_response

        # Проверка команд режима
        if any(word in normalized_message for word in ['кратко', 'покороче', 'сократи']):
            self.conversation_mode = "brief"
            return "✅ Перехожу в краткий режим. Буду отвечать покороче!"
        
        if any(word in normalized_message for word in ['подробно', 'подробнее', 'детали']):
            self.conversation_mode = "detailed"
            return "✅ Перехожу в подробный режим. Буду давать развернутые ответы!"

        if normalized_message in self.qa_database:
            response = self.qa_database[normalized_message]
            
            key_topics = {
                'искусственный интеллект': ['нейросети', 'машинное обучение', 'применение'],
                'машинное обучение': ['алгоритмы', 'типы обучения', 'практика'],
                'нейросети': ['типы сетей', 'обучение', 'применение'],
                'python': ['основы', 'продвинутые темы', 'проекты']
            }
            
            if normalized_message in key_topics:
                return self.ask_contextual_question(normalized_message, key_topics[normalized_message])
            
            return response
        
        # Поиск частичного совпадения
        for question, answer in self.qa_database.items():
            if question in normalized_message:
                return answer
        
        return None

    def get_actual_info(self, message):
        """Получение актуальной информации"""
        normalized = self.normalize_message(message)
        
        try:
            if any(word in normalized for word in ['время', 'time', 'который час']):
                current_time = datetime.datetime.now().strftime("%H:%M")
                return f"🕐 Сейчас {current_time}"
            
            elif any(word in normalized for word in ['дата', 'число', 'day', 'date']):
                current_date = datetime.datetime.now().strftime("%d.%m.%Y")
                return f"📅 Сегодня {current_date}"
                
        except Exception as e:
            return None
        
        return None

    def is_math_expression(self, text):
        """Проверка математического выражения"""
        math_patterns = [r'\d+[\+\-\*\/]', r'посчитай', r'вычисли', r'сколько будет', r'реши пример']
        text_lower = self.normalize_message(text)
        return any(re.search(pattern, text_lower) for pattern in math_patterns)

    def advanced_calculate(self, expression):
        """Вычисление математических выражений"""
        try:
            clean_expr = self.normalize_message(expression)
            math_words = ['посчитай', 'вычисли', 'сколько будет', 'реши', 'пример']
            for word in math_words:
                clean_expr = clean_expr.replace(word, '')
            clean_expr = clean_expr.strip()
            
            clean_expr = clean_expr.replace(' ', '')
            clean_expr = clean_expr.replace('пи', str(math.pi))
            clean_expr = clean_expr.replace('^', '**')
            
            allowed_chars = set('0123456789+-*/().')
            expr_chars = clean_expr.replace(' ', '')
            if all(c in allowed_chars for c in expr_chars):
                result = eval(clean_expr)
                return f"🎯 Результат: {result}"
            else:
                return "❌ Не могу вычислить это выражение. Попробуй написать его проще!"
                
        except Exception as e:
            return f"❌ Ошибка в вычислении. Проверь правильность выражения!"

    def search_wikipedia(self, query):
        """Поиск в Wikipedia"""
        simple_phrases = ['как тебя зовут', 'кто ты', 'что делаешь', 'как дела', 'привет', 'пока']
        
        query_lower = query.lower()
        if any(phrase in query_lower for phrase in simple_phrases):
            return None
            
        try:
            search_results = wikipedia.search(query)
            if search_results:
                page = wikipedia.page(search_results[0])
                summary = page.summary
                if self.conversation_mode == "brief":
                    summary = summary.split('.')[0] + '.'
                return f"{summary}\n\nХочешь узнать больше деталей? 📖"
        except:
            pass
        return None

    def generate_creative_text(self, message):
        """Генерация творческих текстов"""
        normalized = self.normalize_message(message)
        
        # Определяем тип запроса
        if any(word in normalized for word in ['напиши стих', 'сочини стихотворение', 'стихи о', 'поэзия']):
            text_type = 'стихи'
        elif any(word in normalized for word in ['напиши рассказ', 'сочини историю', 'придумай сказку']):
            text_type = 'рассказы'
        else:
            return None
        
        # Определяем тему
        theme = None
        for theme_name in self.creative_templates.get(text_type, {}).keys():
            if theme_name in normalized:
                theme = theme_name
                break
        
        # Если тема не указана, выбираем случайную
        if not theme and text_type in self.creative_templates:
            theme = random.choice(list(self.creative_templates[text_type].keys()))
        
        # Генерируем текст
        if text_type and theme and theme in self.creative_templates.get(text_type, {}):
            templates = self.creative_templates[text_type][theme]
            response = random.choice(templates)
            
            if text_type == 'стихи':
                return f"🎭 Вот стихотворение на тему '{theme}':\n\n{response}\n\nХочешь еще стихов? 💫"
            elif text_type == 'рассказы':
                return f"📖 Вот начало рассказа на тему '{theme}':\n\n{response}\n\nПродолжить историю? ✍️"
        
        return None

    def get_pattern_response(self, message):
        """Получение ответа по паттернам"""
        normalized_message = self.normalize_message(message)
        
        for pattern_type, data in self.patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, normalized_message):
                    response = random.choice(data['responses'])
                    return response
        
        return None

    # 🆕 ОБНОВЛЕННЫЙ PROCESS_MESSAGE С ДИАЛОГОВОЙ СИСТЕМОЙ
    def process_message(self, message):
        """Основной метод обработки сообщений"""
        start_time = time.time()
        
        try:
            self.conversation_history.append(('user', message))
            self.last_user_message = message
            
            # 🆕 ПРИОРИТЕТ 1: ДИАЛОГОВАЯ СИСТЕМА
            dialog_response = self.handle_dialog_flow(message)
            if dialog_response:
                self.conversation_history.append(('bot', dialog_response))
                return dialog_response

            # 2. Генерация творческих текстов
            creative_response = self.generate_creative_text(message)
            if creative_response:
                self.conversation_history.append(('bot', creative_response))
                return creative_response

            # 3. Контекстные ответы (старая система)
            contextual_response = self.handle_contextual_response(message)
            if contextual_response:
                self.conversation_history.append(('bot', contextual_response))
                return contextual_response

            # 4. Интеллектуальные паттерны
            pattern_response = self.get_pattern_response(message)
            if pattern_response:
                self.conversation_history.append(('bot', pattern_response))
                return pattern_response

            # 5. Переводчик
            if any(word in self.normalize_message(message) for word in ['перевод', 'translate', 'переведи']):
                text_to_translate = re.sub(r'(перевод|translate|переведи)\s*', '', message, flags=re.IGNORECASE).strip()
                if text_to_translate and len(text_to_translate) > 2:
                    translated = self.translator.translate(text_to_translate)
                    if translated:
                        response = f"🔤 Перевод на английский:\n\"{text_to_translate}\" → \"{translated}\""
                        self.conversation_history.append(('bot', response))
                        return response

            # 6. Актуальная информация
            actual_info = self.get_actual_info(message)
            if actual_info:
                self.conversation_history.append(('bot', actual_info))
                return actual_info

            # 7. QA база
            qa_response = self.find_qa_response(message)
            if qa_response:
                self.conversation_history.append(('bot', qa_response))
                return qa_response

            # 8. Математические выражения
            if self.is_math_expression(message):
                math_response = self.advanced_calculate(message)
                self.conversation_history.append(('bot', math_response))
                return math_response

            # 9. Wikipedia
            wiki_response = self.search_wikipedia(message)
            if wiki_response:
                self.conversation_history.append(('bot', wiki_response))
                return wiki_response
            
            # 10. Умные ответы на основе контекста
            if len(self.conversation_history) >= 3:
                response = "Интересная мысль! 🧠 Расскажи подробнее?"
            else:
                response = "Могу помочь с: ответами, вычислениями, переводом, стихами, рассказами! 💡"
            
            # 🆕 Сбрасываем диалоговое состояние если нет подходящего ответа
            self.reset_dialog_state()
            
        except Exception as e:
            response = "Кажется, произошла небольшая ошибка, но давай продолжим наш интересный разговор! 💫"
            self.reset_dialog_state()
        
        self.conversation_history.append(('bot', response))
        
        response_time = time.time() - start_time
        self.performance_metrics['response_times'].append(response_time)
        
        return response

# GUI КЛАСС (без изменений)
class EnhancedYankaAIGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Yanka AI - Умный помощник")
        
        self.root.geometry("900x700")
        self.root.minsize(600, 400)
        self.root.maxsize(1200, 900)
        
        self.root.configure(bg='#1a1a1a')
        
        self.yanka_ai = UltraYankaAI()
        self.setup_ui()
        self.setup_context_menu()
    
    def setup_context_menu(self):
        """Создает контекстное меню для текстового поля"""
        self.context_menu = Menu(self.root, tearoff=0, bg='#2d2d2d', fg='white')
        self.context_menu.add_command(label="Копировать", command=self.copy_text)
        self.context_menu.add_command(label="Вставить", command=self.paste_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Выделить все", command=self.select_all)
        
        self.chat_area.bind("<Button-3>", self.show_context_menu)
        self.input_entry.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Показывает контекстное меню"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def copy_text(self):
        """Копирует выделенный текст"""
        try:
            widget = self.root.focus_get()
            if hasattr(widget, 'get'):
                selected_text = widget.selection_get()
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
            else:
                selected_text = widget.get("sel.first", "sel.last")
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
        except:
            pass
    
    def paste_text(self):
        """Вставляет текст из буфера обмена"""
        try:
            widget = self.root.focus_get()
            clipboard_text = self.root.clipboard_get()
            
            if hasattr(widget, 'insert'):
                if hasattr(widget, 'get'):
                    widget.insert(tk.INSERT, clipboard_text)
                else:
                    widget.insert(tk.INSERT, clipboard_text)
        except:
            pass
    
    def select_all(self):
        """Выделяет весь текст в активном виджете"""
        try:
            widget = self.root.focus_get()
            if hasattr(widget, 'tag_add'):
                widget.tag_add("sel", "1.0", "end")
            elif hasattr(widget, 'select_range'):
                widget.select_range(0, tk.END)
        except:
            pass
    
    def setup_ui(self):
        self.colors = {
            'bg': '#1a1a1a', 'chat_bg': '#2d2d2d', 'input_bg': '#3d3d3d',
            'text': '#ffffff', 'accent': '#00ff88'
        }
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(
            main_frame, text="Yanka AI", font=('Arial', 16, 'bold'),
            bg=self.colors['bg'], fg=self.colors['accent'], pady=10
        )
        title_label.pack(fill=tk.X)
        
        self.chat_area = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, font=('Arial', 11),
            bg=self.colors['chat_bg'], fg=self.colors['text'],
            padx=15, pady=15, insertbackground=self.colors['text'],
            relief='flat'
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_area.config(state=tk.DISABLED)
        
        input_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        input_frame.pack(fill=tk.X)
        
        self.input_entry = tk.Entry(
            input_frame, font=('Arial', 12), bg=self.colors['input_bg'], 
            fg=self.colors['text'], relief='flat'
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.input_entry.bind('<Return>', lambda event: self.send_message())
        self.input_entry.focus()
        
        self.send_button = tk.Button(
            input_frame, text="➤", command=self.send_message,
            font=('Arial', 14, 'bold'), bg=self.colors['accent'], 
            fg=self.colors['bg'], relief='flat', width=3
        )
        self.send_button.pack(side=tk.RIGHT)
        
        self.setup_keyboard_shortcuts()
        
        self.show_welcome_message()
    
    def setup_keyboard_shortcuts(self):
        """Настройка горячих клавиш"""
        self.root.bind('<Control-c>', lambda e: self.copy_text())
        self.root.bind('<Control-v>', lambda e: self.paste_text())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        self.root.bind('<Control-Return>', lambda e: self.send_message())
    
    def add_message(self, sender, message, msg_type="user"):
        self.chat_area.config(state=tk.NORMAL)
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        if msg_type == "user":
            self.chat_area.insert(tk.END, f"[{timestamp}] Вы: {message}\n\n")
        else:
            self.chat_area.insert(tk.END, f"[{timestamp}] Yanka AI: {message}\n\n")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def show_welcome_message(self):
        welcome_text = "Привет! Я Yanka AI. Готов к общению! 😊"
        self.add_message("Yanka AI", welcome_text, "bot")
    
    def send_message(self):
        message = self.input_entry.get().strip()
        if message:
            self.add_message("Вы", message, "user")
            self.input_entry.delete(0, tk.END)
            
            self.send_button.config(state=tk.DISABLED, text="...")
            self.root.after(100, self.process_ai_response, message)
    
    def process_ai_response(self, message):
        try:
            response = self.yanka_ai.process_message(message)
            self.add_message("Yanka AI", response, "bot")
        except Exception as e:
            self.add_message("Yanka AI", "Ошибка обработки", "bot")
        finally:
            self.send_button.config(state=tk.NORMAL, text="➤")

def main():
    root = tk.Tk()
    app = EnhancedYankaAIGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()