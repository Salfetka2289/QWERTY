import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import re
import math
from datetime import datetime
from threading import Thread

class YankaAI:
    def __init__(self):
        self.mood = "creative"
        self.user_name = None
        self.conversation_history = []
        self.user_mood = "neutral"
        self.user_interests = set()
        self.context_memory = {}
        self.conversation_depth = 0
        
        # База для генерации текстов
        self.text_templates = {
            'story': {
                'beginnings': [
                    "В одном далёком городе, где улицы были вымощены звёздной пылью,",
                    "Однажды утром, когда солнце только начинало подниматься над горизонтом,",
                    "В мире, где магия была такой же обычной, как утренний кофе,",
                    "Среди древних руин, хранящих тайны веков,",
                    "В лаборатории, где наука и магия переплетались в танце открытий,"
                ],
                'characters': [
                    "юный изобретатель по имени Алекс",
                    "мудрая старушка с глазами, полными загадок",
                    "бесстрашный исследователь космоса",
                    "таинственный незнакомец с прошлым, окутанным тайной",
                    "обычный студент, обнаруживший необычные способности"
                ],
                'actions': [
                    "обнаружил древний артефакт, способный изменять реальность",
                    "столкнулся с загадкой, которая изменила его жизнь навсегда",
                    "отправился в путешествие, чтобы найти ответы на вечные вопросы",
                    "наткнулся на дверь в другой мир, скрытую в обычной библиотеке",
                    "начал слышать голоса, которые могли предсказывать будущее"
                ],
                'endings': [
                    "и понял, что настоящее приключение только начинается.",
                    "но это была лишь первая глава в истории, которая изменит всё.",
                    "и с этого момента его мир уже никогда не будет прежним.",
                    "открывая путь к новым открытиям и невероятным возможностям.",
                    "доказывая, что магия есть в каждом из нас, нужно лишь поверить."
                ]
            },
            'poem': {
                'themes': ['любовь', 'природа', 'город', 'время', 'мечты', 'одиночество', 'надежда'],
                'structures': [
                    ["Утром", "днём", "вечером", "ночью"],
                    ["Весной", "летом", "осенью", "зимой"],
                    ["В детстве", "в юности", "в зрелости", "в старости"]
                ],
                'lines': [
                    "Тихий шепот ветра в ночи",
                    "Звёзды падают в ладони реки",
                    "Город спит под покровом теней",
                    "Время течёт как песок сквозь пальцы",
                    "Сердце бьётся в ритме вселенной"
                ]
            },
            'advice': {
                'topics': ['отношения', 'работа', 'творчество', 'здоровье', 'развитие'],
                'openings': [
                    "Иногда самое важное - это",
                    "Помни, что истинная сила в",
                    "Не бойся меняться, ведь",
                    "Самое ценное, что ты можешь сделать - это",
                    "В трудные времена важно"
                ],
                'advices': [
                    "прислушиваться к своему сердцу и следовать за мечтой",
                    "находить радость в маленьких моментах каждый день",
                    "быть честным с собой и окружающими",
                    "не бояться начинать сначала, когда это необходимо",
                    "ценить тех, кто действительно заботится о тебе"
                ]
            }
        }

        # Расширенная база знаний
        self.knowledge_patterns = {
            'greeting': {
                'patterns': [r'привет', r'здравствуй', r'добрый', r'хай', r'ку', r'здорово', r'салют'],
                'responses': [
                    "Привет! ✨ Готов к творчеству и общению!",
                    "Здравствуй! 🚀 Чем займёмся сегодня?",
                    "Привет! 💫 Расскажи, что на уме?"
                ]
            },
            
            'generate_text': {
                'patterns': [r'напиши', r'создай', r'придумай', r'сгенерируй', r'сочини'],
                'responses': [
                    "Отличная идея! Вот что у меня получилось:\n\n{text}",
                    "С удовольствием! Посмотри на этот текст:\n\n{text}",
                    "Вот мой творческий вариант:\n\n{text}"
                ]
            },
            
            'dog_names': {
                'patterns': [r'как назвать собаку', r'имя для собаки', r'кличка'],
                'responses': [
                    "Для {gender} отлично подойдёт {name}! 🐕",
                    "Как насчёт {name}? Звучит прекрасно!",
                    "Мне нравится {name}! Отличный выбор! 🐶"
                ]
            },
            
            'activities': {
                'patterns': [r'чем заняться', r'что делать', r'скучно'],
                'responses': [
                    "Попробуй {activity}! {mood_comment}",
                    "Как насчёт {activity}? {mood_comment}",
                    "Предлагаю {activity}! {mood_comment}"
                ]
            },
            
            'math': {
                'patterns': [r'посчитай', r'вычисли', r'сколько будет'],
                'responses': [
                    "Конечно! {result} 🧮",
                    "Вот результат: {result} ✅",
                    "Получилось: {result} ✨"
                ]
            }
        }

        # Базы данных
        self.dog_names = {
            "male": ["Арчи", "Бэйли", "Чарли", "Джейк", "Макс", "Оскар", "Рокки", "Тедди"],
            "female": ["Луна", "Белла", "Молли", "Лола", "Зоя", "Рокси", "Сэди", "Вилли"],
            "funny": ["Пончик", "Бублик", "Кекс", "Пирожок", "Вафля", "Котлета", "Суши"]
        }
        
        self.activities_db = {
            "creative": ["написать короткий рассказ", "сочинить стихотворение", "нарисовать эскиз", 
                        "сделать фотоколлаж", "записать голосовую заметку"],
            "active": ["прогуляться в парке", "сделать зарядку", "потанцевать под музыку", 
                      "покататься на велосипеде", "сходить в бассейн"],
            "educational": ["почитать книгу", "посмотреть документальный фильм", 
                           "изучить новую тему", "пройти онлайн-курс"],
            "social": ["позвонить другу", "написать письмо", "встретиться с близкими"]
        }

    def generate_story(self):
        """Генерирует короткий рассказ"""
        beginning = random.choice(self.text_templates['story']['beginnings'])
        character = random.choice(self.text_templates['story']['characters'])
        action = random.choice(self.text_templates['story']['actions'])
        ending = random.choice(self.text_templates['story']['endings'])
        
        return f"{beginning} {character} {action} {ending}"

    def generate_poem(self):
        """Генерирует короткое стихотворение"""
        theme = random.choice(self.text_templates['poem']['themes'])
        structure = random.choice(self.text_templates['poem']['structures'])
        lines = random.sample(self.text_templates['poem']['lines'], 3)
        
        poem = f"О {theme}...\n\n"
        for i, line in enumerate(lines):
            poem += f"{line}\n"
        poem += f"\n{random.choice(structure)} всегда найдётся место чуду."
        
        return poem

    def generate_advice(self):
        """Генерирует совет"""
        topic = random.choice(self.text_templates['advice']['topics'])
        opening = random.choice(self.text_templates['advice']['openings'])
        advice = random.choice(self.text_templates['advice']['advices'])
        
        return f"О {topic}:\n\n{opening} {advice}."

    def analyze_user_input(self, text):
        """Анализ ввода пользователя"""
        text_lower = text.lower()
        
        topics = []
        for category, data in self.knowledge_patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, text_lower):
                    topics.append(category)
        
        entities = {
            'gender': 'мальчик' if any(word in text_lower for word in ['мальчик', 'пса']) else 
                     'девочка' if any(word in text_lower for word in ['девочка', 'суку']) else None,
            'math_expression': re.search(r'[\d+\-*/().]+', text) if any(char in text for char in '+-*/') else None,
            'text_type': 'story' if any(word in text_lower for word in ['рассказ', 'историю', 'story']) else
                        'poem' if any(word in text_lower for word in ['стих', 'поэм', 'poem']) else
                        'advice' if any(word in text_lower for word in ['совет', 'рекомендац']) else 'random'
        }
        
        return {
            'topics': topics,
            'entities': entities
        }

    def generate_text_response(self, text_type):
        """Генерирует текстовый ответ"""
        if text_type == 'story':
            return self.generate_story()
        elif text_type == 'poem':
            return self.generate_poem()
        elif text_type == 'advice':
            return self.generate_advice()
        else:
            # Случайный выбор
            return random.choice([
                self.generate_story(),
                self.generate_poem(),
                self.generate_advice()
            ])

    def calculate_expression(self, expression):
        """Вычисление математических выражений"""
        try:
            expression = expression.replace('х', '*').replace('Х', '*')
            expression = re.sub(r'\s+', '', expression)
            result = eval(expression)
            return f"{expression} = {result}"
        except:
            return "Не могу вычислить это выражение"

    def get_response(self, user_input):
        """Основная функция получения ответа"""
        analysis = self.analyze_user_input(user_input)
        
        # Сохраняем в историю
        self.conversation_history.append((user_input, ""))
        if len(self.conversation_history) > 10:
            self.conversation_history.pop(0)
        
        # Генерация текста
        if 'generate_text' in analysis['topics']:
            text_type = analysis['entities']['text_type']
            generated_text = self.generate_text_response(text_type)
            base_response = random.choice(self.knowledge_patterns['generate_text']['responses'])
            return base_response.format(text=generated_text)
        
        # Имена для собак
        elif 'dog_names' in analysis['topics']:
            gender = analysis['entities']['gender'] or random.choice(['мальчик', 'девочка'])
            name = random.choice(self.dog_names['male' if gender == 'мальчик' else 'female'])
            base_response = random.choice(self.knowledge_patterns['dog_names']['responses'])
            return base_response.format(gender=gender, name=name)
        
        # Математика
        elif 'math' in analysis['topics'] and analysis['entities']['math_expression']:
            result = self.calculate_expression(analysis['entities']['math_expression'].group())
            base_response = random.choice(self.knowledge_patterns['math']['responses'])
            return base_response.format(result=result)
        
        # Занятия
        elif 'activities' in analysis['topics']:
            activity_type = random.choice(list(self.activities_db.keys()))
            activity = random.choice(self.activities_db[activity_type])
            base_response = random.choice(self.knowledge_patterns['activities']['responses'])
            return base_response.format(activity=activity, mood_comment="Думаю, тебе понравится!")
        
        # Приветствие
        elif 'greeting' in analysis['topics']:
            return random.choice(self.knowledge_patterns['greeting']['responses'])
        
        # Случайная генерация текста
        else:
            return self.generate_text_response('random')

class ModernChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Yanka AI")
        self.root.geometry("800x700")
        self.root.configure(bg='#0F172A')
        
        # Современная цветовая схема
        self.colors = {
            'primary': '#6366F1',
            'secondary': '#8B5CF6',
            'accent': '#06D6A0',
            'background': '#0F172A',
            'surface': '#1E293B',
            'text_primary': '#F1F5F9',
            'text_secondary': '#94A3B8'
        }
        
        self.bot = YankaAI()
        self.setup_modern_ui()
    
    def setup_modern_ui(self):
        # Шрифты
        self.font_primary = ("Segoe UI", 11)
        self.font_secondary = ("Segoe UI", 9)
        self.font_title = ("Segoe UI", 16, "bold")
        
        # Заголовок
        header_frame = tk.Frame(self.root, bg=self.colors['background'], height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Yanka AI",
            font=self.font_title,
            bg=self.colors['background'],
            fg=self.colors['text_primary']
        )
        title_label.pack(side=tk.LEFT, padx=25, pady=15)
        
        status_label = tk.Label(
            header_frame,
            text="🟢 Онлайн",
            font=self.font_secondary,
            bg=self.colors['background'],
            fg='#10B981'
        )
        status_label.pack(side=tk.RIGHT, padx=25, pady=15)
        
        # Основная область чата
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Область сообщений
        self.chat_frame = tk.Frame(main_frame, bg=self.colors['surface'], bd=0, relief='flat')
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chat_area = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            font=self.font_primary,
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=20,
            insertbackground=self.colors['text_primary']
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        # Панель ввода - ЯВНО ВИДИМАЯ
        input_frame = tk.Frame(self.root, bg=self.colors['background'], height=80)
        input_frame.pack(fill=tk.X, padx=20, pady=15)
        input_frame.pack_propagate(False)
        
        # Поле ввода - ЯВНО ВИДИМОЕ
        self.input_entry = tk.Entry(
            input_frame,
            font=self.font_primary,
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            relief='flat',
            bd=0,
            insertbackground=self.colors['text_primary'],
            width=50  # Явно задаем ширину
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        self.input_entry.bind('<Return>', lambda event: self.send_message())
        self.input_entry.focus()
        
        # Стилизация поля ввода
        self.input_entry.configure(
            highlightthickness=1,
            highlightbackground=self.colors['secondary'],
            highlightcolor=self.colors['primary']
        )
        
        # Кнопка отправки - ЯВНО ВИДИМАЯ
        send_button = tk.Button(
            input_frame,
            text="Отправить",
            command=self.send_message,
            font=self.font_primary,
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            bd=0,
            padx=25,
            pady=8,
            cursor='hand2'
        )
        send_button.pack(side=tk.RIGHT)
        
        # Эффекты при наведении
        def on_enter(e):
            send_button.configure(bg=self.colors['secondary'])
        
        def on_leave(e):
            send_button.configure(bg=self.colors['primary'])
        
        send_button.bind("<Enter>", on_enter)
        send_button.bind("<Leave>", on_leave)
        
        # Панель быстрых действий - ЯВНО ВИДИМАЯ
        quick_actions_frame = tk.Frame(self.root, bg=self.colors['background'], height=50)
        quick_actions_frame.pack(fill=tk.X, padx=20, pady=10)
        quick_actions_frame.pack_propagate(False)
        
        quick_actions = [
            ("📖 Рассказ", "напиши рассказ"),
            ("🎭 Стих", "напиши стихотворение"),
            ("💡 Совет", "дай совет"),
            ("🐶 Имя", "как назвать собаку"),
            ("🧮 Считать", "посчитай 2+2*3")
        ]
        
        for text, command in quick_actions:
            btn = tk.Button(
                quick_actions_frame,
                text=text,
                command=lambda cmd=command: self.quick_action(cmd),
                font=self.font_secondary,
                bg=self.colors['surface'],
                fg=self.colors['text_secondary'],
                relief='flat',
                bd=0,
                padx=12,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['primary'], fg='white'))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(
                bg=self.colors['surface'], 
                fg=self.colors['text_secondary']
            ))

    def quick_action(self, command):
        """Быстрые действия"""
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, command)
        self.send_message()

    def display_message(self, sender, message, msg_type="user"):
        """Отображение сообщений"""
        self.chat_area.config(state=tk.NORMAL)
        
        if msg_type == "user":
            # Сообщение пользователя
            self.chat_area.insert(tk.END, f"Вы: ", "user_name")
            self.chat_area.insert(tk.END, f"{message}\n\n", "user_msg")
        else:
            # Сообщение бота
            self.chat_area.insert(tk.END, f"Yanka AI: ", "bot_name")
            self.chat_area.insert(tk.END, f"{message}\n\n", "bot_msg")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def send_message(self):
        user_input = self.input_entry.get().strip()
        
        if user_input:
            self.display_message("Вы", user_input, "user")
            self.input_entry.delete(0, tk.END)
            
            # Индикатор набора
            self.display_message("Yanka AI", "✨ Думаю...", "bot")
            
            Thread(target=self.get_bot_response, args=(user_input,), daemon=True).start()
    
    def get_bot_response(self, user_input):
        response = self.bot.get_response(user_input)
        self.root.after(0, self.replace_last_message, response)
    
    def replace_last_message(self, response):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete('end-3l', 'end-1l')
        self.display_message("Yanka AI", response, "bot")

def main():
    root = tk.Tk()
    app = ModernChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()